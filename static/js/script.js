document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const storyForm = document.getElementById('storySetupForm');
    const storyDisplay = document.getElementById('storyDisplay');
    const currentStory = document.getElementById('currentStory');
    const choicesContainer = document.getElementById('choicesContainer');
    const storyHistory = document.getElementById('storyHistory');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const restartBtn = document.getElementById('restartBtn');

    // Story State
    let currentStoryState = {
        setting: '',
        character: '',
        goal: '',
        history: []
    };

    // Form Submission Handler
    storyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        currentStoryState.setting = document.getElementById('setting').value;
        currentStoryState.character = document.getElementById('character').value;
        currentStoryState.goal = document.getElementById('goal').value;

        storyForm.classList.add('hidden');
        storyDisplay.classList.remove('hidden');
        restartBtn.classList.remove('hidden');

        await generateStory();
    });

    // Generate story content
    async function generateStory(previousChoice = null) {
        loadingSpinner.classList.remove('hidden');
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    setting: currentStoryState.setting,
                    character: currentStoryState.character,
                    goal: currentStoryState.goal,
                    choice: previousChoice
                })
            });

            const data = await response.json();
            typewriterEffect(currentStory, data.text);
            createChoiceButtons(data.choices);
            
        } catch (error) {
            console.error('Error generating story:', error);
            currentStory.textContent = 'Our tale has encountered a mysterious force... Please try again.';
        }
        
        loadingSpinner.classList.add('hidden');
    }

    // Handle choice selection
    async function handleChoice(choice) {
        loadingSpinner.classList.remove('hidden');
        logToHistory(currentStory.textContent, choice);
        await generateStory(choice);
        loadingSpinner.classList.add('hidden');
    }

    // Create choice buttons
    function createChoiceButtons(choices) {
        choicesContainer.innerHTML = '';
        
        choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice;
            button.addEventListener('click', () => handleChoice(choice));
            choicesContainer.appendChild(button);
        });
    }

    // Add story segments to history
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

    // Typewriter text effect
    function typewriterEffect(element, text, speed = 50) {
        if (element._typingInterval) {
            clearInterval(element._typingInterval);
        }
        element.textContent = '';
        let i = 0;
        
        element._typingInterval = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(element._typingInterval);
            }
        }, speed);
    }

    // Reset game state
    restartBtn.addEventListener('click', () => {
        currentStoryState = {
            setting: '',
            character: '',
            goal: '',
            history: []
        };
        storyForm.reset();
        storyHistory.innerHTML = '';
        storyDisplay.classList.add('hidden');
        storyForm.classList.remove('hidden');
        restartBtn.classList.add('hidden');
    });
});