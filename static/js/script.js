document.addEventListener('DOMContentLoaded', () => {
    const storyForm = document.getElementById('storySetupForm');
    const storyDisplay = document.getElementById('storyDisplay');
    const currentStory = document.getElementById('currentStory');
    const choicesContainer = document.getElementById('choicesContainer');
    const storyHistory = document.getElementById('storyHistory');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const restartBtn = document.getElementById('restartBtn');

    let currentStoryState = {
        setting: '',
        character: '',
        goal: '',
        fullText: '',
        history: []
    };

    let storySoFar = '';

    storyForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        currentStoryState.setting = document.getElementById('setting').value;
        currentStoryState.character = document.getElementById('character').value;
        currentStoryState.goal = document.getElementById('goal').value;
        currentStoryState.fullText = '';
        storySoFar = '';

        storyForm.classList.add('hidden');
        storyDisplay.classList.remove('hidden');
        restartBtn.classList.remove('hidden');

        await generateStory();
    });

    async function generateStory() {
    loadingSpinner.classList.remove('hidden');

    // 🔧 Clear any leftover choices from previous stories
    choicesContainer.innerHTML = '';
    choicesContainer.classList.add('hidden');

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                setting: currentStoryState.setting,
                character: currentStoryState.character,
                goal: currentStoryState.goal
            })
        });

        const data = await response.json();
        currentStoryState.fullText = data.text;
        storySoFar = data.text + '\n';

        typewriterEffect(currentStory, data.text, 20, () => {
            createChoiceButtons(data.choices);
            choicesContainer.classList.remove('hidden');
        });

    } catch (error) {
        console.error('Error generating story:', error);
        currentStory.textContent = 'Our tale has encountered a mysterious force... Please try again.';
    }

    loadingSpinner.classList.add('hidden');
}


    async function handleChoice(choice) {
        loadingSpinner.classList.remove('hidden');
        logToHistory(currentStory.textContent, choice);

        // Immediately hide and clear choices
        choicesContainer.innerHTML = '';
        choicesContainer.classList.add('hidden');

        try {
            const response = await fetch('/continue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    story: currentStoryState.fullText,
                    choice: choice,
                    goal: currentStoryState.goal
                })
            });

            const data = await response.json();
            currentStoryState.fullText += '\n\n' + data.text;
            storySoFar += data.text + '\n';

            if (data.ending) {
                typewriterEffect(currentStory, data.text, 20, () => {
                    setTimeout(() => {
                        document.body.classList.add('fade-out');
                        setTimeout(() => {
                            fetch('/ending', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ story: currentStoryState.fullText })
                            })
                            .then(res => res.text())
                            .then(html => {
                                document.open();
                                document.write(html);
                                document.close();
                            });
                        }, 500);
                    }, 1200);
                });
            } else {
                typewriterEffect(currentStory, data.text, 20, () => {
                    createChoiceButtons(data.choices);
                    choicesContainer.classList.remove('hidden');
                });
            }

        } catch (error) {
            console.error('Error continuing story:', error);
            currentStory.textContent = 'The path forward is unclear... Try again.';
        }

        loadingSpinner.classList.add('hidden');
    }

    function createChoiceButtons(choices) {
        choicesContainer.innerHTML = '';
        choicesContainer.classList.remove('hidden');

        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice;
            button.disabled = true;

            button.addEventListener('click', () => handleChoice(choice));
            choicesContainer.appendChild(button);

            // Staggered animation: add `.show` class with delay
            setTimeout(() => {
                button.classList.add('show');
            }, 100 * index);
        });

        const totalDelay = 100 * choices.length;
        setTimeout(() => enableChoiceButtons(), totalDelay + 500);
    }

    function disableChoiceButtons() {
        const buttons = document.querySelectorAll('.choice-btn');
        buttons.forEach(btn => btn.disabled = true);
    }

    function enableChoiceButtons() {
        const buttons = document.querySelectorAll('.choice-btn');
        buttons.forEach(btn => btn.disabled = false);
    }

    function logToHistory(storyText, choice) {
        const historyEntry = document.createElement('div');
        historyEntry.className = 'history-entry';
        historyEntry.innerHTML = `
            <p class="history-text">${storyText}</p>
            ${choice ? `<p class="history-choice">➥ ${choice}</p>` : ''}
        `;
        storyHistory.appendChild(historyEntry);
        storyHistory.scrollTop = storyHistory.scrollHeight;
    }

    function typewriterEffect(element, text, speed = 20, callback) {
        if (element._typingInterval) {
            clearInterval(element._typingInterval);
        }
        element.textContent = '';
        let i = 0;

        // Hide choices while typing
        choicesContainer.classList.add('hidden');

        element._typingInterval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(element._typingInterval);
                if (typeof callback === 'function') callback();
                enableChoiceButtons();
            }
        }, speed);
    }

    restartBtn.addEventListener('click', () => {
        currentStoryState = {
            setting: '',
            character: '',
            goal: '',
            fullText: '',
            history: []
        };
        storySoFar = '';
        storyForm.reset();
        storyHistory.innerHTML = '';
        storyDisplay.classList.add('hidden');
        storyForm.classList.remove('hidden');
        restartBtn.classList.add('hidden');
    });
});

