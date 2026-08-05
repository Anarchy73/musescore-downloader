// ==UserScript==
// @name         PostUrlsFromMuse
// @version      2026-02-27
// @description  Get all the sheets (Preserve S3 Tokens Fix)
// @author       Anarchy73
// @match        https://musescore.com/*/scores/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @grant        GM_xmlhttpRequest
// @connect      *
// ==/UserScript==

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchImageAsBase64(url) {
    return new Promise((resolve, reject) => {
        GM_xmlhttpRequest({
            method: "GET",
            url: url,
            responseType: "blob",
            headers: {
                "Referer": window.location.href,
                "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
            },
            onload: function(response) {
                if (response.status === 200) {
                    let reader = new FileReader();
                    reader.onloadend = function() {
                        resolve(reader.result);
                    }
                    reader.readAsDataURL(response.response);
                } else {
                    reject(`Ошибка HTTP ${response.status} при скачивании ${url}`);
                }
            },
            onerror: function(err) {
                reject(err);
            }
        });
    });
}

(async function() {
    'use strict';

    await sleep(2000);
    console.log("Анализ структуры страницы...");

    let mainScroller = window;
    let maxWidth = 0;

    for (let div of document.querySelectorAll('div')) {
        if (div.scrollHeight > div.clientHeight + 10) {
            let width = div.getBoundingClientRect().width;
            if (width > maxWidth) {
                maxWidth = width;
                mainScroller = div;
            }
        }
    }

    let scoreHash = null;
    // Используем Map: ключ — чистая ссылка (для защиты от дублей), значение — полная ссылка с токеном
    let collectedScores = new Map();

    function harvestVisibleScores() {
        const images = document.querySelectorAll('img');
        for (let img of images) {
            if (!img.src || !img.src.includes('scoredata')) continue;

            if (!scoreHash && img.getBoundingClientRect().width > 400) {
                let match = img.src.match(/scoredata\/[^\/]+\/([a-f0-9]+)\//);
                if (match) scoreHash = match[1];
            }

            let isMainScore = false;
            if (scoreHash) {
                if (img.src.includes(scoreHash)) isMainScore = true;
            } else {
                if (img.getBoundingClientRect().width > 400) isMainScore = true;
            }

            if (isMainScore) {
                let fullUrl = img.src; // Сохраняем токен!
                let baseUrl = fullUrl.split('?')[0].split('@')[0]; // База только для фильтрации

                if (!collectedScores.has(baseUrl)) {
                    collectedScores.set(baseUrl, fullUrl);
                }
            }
        }
    }

    let stuckCounter = 0;
    let lastScrollPos = -1;
    console.log("Начинаем прокрутку и сбор ссылок...");

    while (stuckCounter < 4) {
        harvestVisibleScores();
        if (mainScroller === window) {
            window.scrollBy(0, 800);
            if (window.scrollY === lastScrollPos) stuckCounter++;
            else { stuckCounter = 0; lastScrollPos = window.scrollY; }
        } else {
            mainScroller.scrollBy(0, 800);
            if (mainScroller.scrollTop === lastScrollPos) stuckCounter++;
            else { stuckCounter = 0; lastScrollPos = mainScroller.scrollTop; }
        }
        await sleep(600);
    }

    harvestVisibleScores();

    // Превращаем словарь в массив и сортируем
    let srcs = Array.from(collectedScores.entries()).sort((a, b) => {
        let numA = parseInt((a[0].match(/score_(\d+)/) || [0, 0])[1]);
        let numB = parseInt((b[0].match(/score_(\d+)/) || [0, 0])[1]);
        return numA - numB;
    });

    console.log(`Найдено страниц нот: ${srcs.length}. Начинаем скачивание...`);

    if (srcs.length === 0) return;

    let payloadFiles = [];
    for (let i = 0; i < srcs.length; i++) {
        let baseUrl = srcs[i][0];
        let fullUrl = srcs[i][1]; // Берем ссылку с секретным токеном Amazon

        try {
            console.log(`Качаем ${i+1}/${srcs.length}...`);
            let base64Data = await fetchImageAsBase64(fullUrl);

            let ext = baseUrl.includes('.svg') ? '.svg' : '.png';
            payloadFiles.push({
                filename: `source_${i}${ext}`,
                content_base64: base64Data
            });
        } catch (e) {
            console.error(`Сбой при скачивании страницы ${i+1}:`, e);
        }
    }

    if (payloadFiles.length !== srcs.length) {
        console.warn(`Внимание! Найдено ${srcs.length} ссылок, но скачано только ${payloadFiles.length}.`);
    }

    console.log("Отправляем на локальный сервер для сборки PDF...");

    GM_xmlhttpRequest({
        method: "POST",
        url: "http://localhost:8000/pdf/",
        headers: {
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({ files: payloadFiles }),
        onload: function(response) {
            console.log("Ответ сервера:", response.responseText);
            alert("Партитура успешно скачана и собрана в PDF!");
        },
        onerror: function(error) {
            console.error("Ошибка при отправке на localhost.", error);
        }
    });
})();
