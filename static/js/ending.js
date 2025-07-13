document.addEventListener('DOMContentLoaded', function () {
    // Get and validate story text
    const storyDataElem = document.getElementById('ending-story-data');
    console.log("Story Data Element:", storyDataElem);

    // Get the raw text and decode any HTML entities
    let storyText = storyDataElem ? (storyDataElem.innerText || storyDataElem.textContent || '') : '';
    const textArea = document.createElement('textarea');
    textArea.innerHTML = storyText;
    storyText = textArea.value;

    console.log("Raw Story Text:", storyText);

    // Clean up the text and split into paragraphs
    storyText = storyText.replace(/\\n/g, '\n').replace(/\n\s*\n/g, '\n\n').trim();
    let paragraphs = storyText.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
    console.log("Processed Paragraphs:", paragraphs);

    // Format paragraphs with proper spacing, indentation, and styling
    paragraphs = paragraphs.map(p => {
        return `<div class="paragraph mb-6">
            <p class="text-justify leading-relaxed" style="text-indent: 2em;">
                <span class="first-letter text-lg font-bold text-purple-300">${p.charAt(0)}</span>${p.slice(1)}
            </p>
        </div>`;
    });

    // Split content into pages (approx. 250 words per page)
    let pages = [];
    let currentPage = [];
    let wordCount = 0;
    const wordsPerPage = 250;

    paragraphs.forEach(paragraph => {
        const words = paragraph.replace(/<[^>]*>/g, '').split(/\s+/).length;

        if (wordCount + words > wordsPerPage) {
            if (currentPage.length > 0) {
                pages.push(currentPage.join('\n'));
                currentPage = [paragraph];
                wordCount = words;
            } else {
                currentPage.push(paragraph);
                pages.push(currentPage.join('\n'));
                currentPage = [];
                wordCount = 0;
            }
        } else {
            currentPage.push(paragraph);
            wordCount += words;
        }
    });

    if (currentPage.length > 0) {
        pages.push(currentPage.join('\n'));
    }

    // Group pages into spreads (2 pages per spread)
    let spreads = [];
    for (let i = 0; i < pages.length; i += 2) {
        spreads.push([pages[i], pages[i + 1] || '']);
    }

    let currentSpread = 0;
    const leftPage = document.getElementById('left-page').querySelector('.page-content');
    const rightPage = document.getElementById('right-page').querySelector('.page-content');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    function renderSpread() {
        const leftIndex = currentSpread * 2;
        const rightIndex = leftIndex + 1;

        leftPage.innerHTML = spreads[currentSpread][0] +
            `<div class="text-right mt-4 text-sm text-gray-400">Page ${leftIndex + 1}</div>`;

        rightPage.innerHTML = spreads[currentSpread][1] +
            (spreads[currentSpread][1] ? `<div class="text-right mt-4 text-sm text-gray-400">Page ${rightIndex + 1}</div>` : '');

        leftPage.parentElement.classList.remove('flipped');
        rightPage.parentElement.classList.remove('flipped');

        prevBtn.style.display = currentSpread === 0 ? 'none' : '';
        nextBtn.style.display = currentSpread === spreads.length - 1 ? 'none' : '';
    }

    prevBtn.addEventListener('click', function () {
        if (currentSpread > 0) {
            leftPage.parentElement.classList.add('flipped');
            rightPage.parentElement.classList.add('flipped');
            setTimeout(() => {
                currentSpread--;
                renderSpread();
            }, 300);
        }
    });

    nextBtn.addEventListener('click', function () {
        if (currentSpread < spreads.length - 1) {
            leftPage.parentElement.classList.add('flipped');
            rightPage.parentElement.classList.add('flipped');
            setTimeout(() => {
                currentSpread++;
                renderSpread();
            }, 300);
        }
    });

    // Initial render
    renderSpread();
});
