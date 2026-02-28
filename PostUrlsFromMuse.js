// ==UserScript==
// @name         PostUrlsFromMuse
// @version      2026-02-27
// @description  Get all the sheets!
// @author       Anarchy73
// @match        https://musescore.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @grant        GM_xmlhttpRequest
// ==/UserScript==
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
(async function() {
    'use strict';
    await sleep(1000);
    const elements = document.querySelectorAll('.A8huy');
    console.log(elements);
    let srcs = []
    for (const element of elements){
        element.scrollIntoView({
            behavior: 'auto',
            block: 'center',
        });
        await sleep(1000);
        srcs.push(element.querySelector('.MHaWn').src);
    }
    console.log(srcs);
    GM_xmlhttpRequest({
        method: "POST",
        url: "http://localhost:8000/pdf",
        headers: {
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(srcs),
        onload: function(response) {
            console.log("Данные отправлены:", response.responseText);
        }
    });
})();