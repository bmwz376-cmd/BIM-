// 言語切り替えボタンを追加
document.addEventListener('DOMContentLoaded', function() {
    // 現在のパスから言語を判定
    const currentPath = window.location.pathname;
    const isEnglish = currentPath.includes('/en/');
    
    // 言語切り替えボタンのHTML
    const switcherHTML = `
        <div class="language-switcher">
            <a href="${isEnglish ? currentPath.replace('/en/', '/') : '/'}" 
               class="${!isEnglish ? 'active' : ''}"
               title="日本語">
                🇯🇵 日本語
            </a>
            <a href="${isEnglish ? currentPath : '/en' + currentPath}" 
               class="${isEnglish ? 'active' : ''}"
               title="English">
                🇬🇧 English
            </a>
        </div>
    `;
    
    // ボディに追加
    const switcher = document.createElement('div');
    switcher.innerHTML = switcherHTML;
    document.body.appendChild(switcher.firstElementChild);
});
