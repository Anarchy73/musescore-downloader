// ==UserScript==
// @name         PostUrlsFromMuse
// @version      2026-02-27
// @description  Get all the sheets!
// @author       You
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

    for (const element of elements){
        element.scrollIntoView({
            behavior: 'auto',
            block: 'center',
        });
        await sleep(1000);
        console.log(element.querySelector('.MHaWn').src);
    }
})();