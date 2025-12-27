// 言語切り替えボタンを追加
document.addEventListener('DOMContentLoaded', function() {
    // 現在のパスから言語を判定
    const currentPath = window.location.pathname;
    const isEnglish = currentPath.includes('/en/');
    
    // ベースパスを取得（GitHub Pagesのリポジトリ名を考慮）
    const basePath = currentPath.split('/').slice(0, 2).join('/') + '/';
    
    // 日本語版と英語版のURL生成
    let jaUrl, enUrl;
    
    if (isEnglish) {
        // 英語版 → 日本語版
        const relativePath = currentPath.replace(/^\/[^/]+\/en\//, '');
        jaUrl = basePath + relativePath;
        enUrl = currentPath;
    } else {
        // 日本語版 → 英語版
        const relativePath = currentPath.replace(/^\/[^/]+\//, '');
        jaUrl = currentPath;
        enUrl = basePath + 'en/' + relativePath;
    }
    
    // 言語切り替えボタンのHTML
    const switcherHTML = `
        <div class="language-switcher">
            <a href="${jaUrl}" 
               class="${!isEnglish ? 'active' : ''}"
               title="日本語">
                🇯🇵 日本語
            </a>
            <a href="${enUrl}" 
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
