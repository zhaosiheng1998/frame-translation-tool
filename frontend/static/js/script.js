document.addEventListener('DOMContentLoaded', function() {
    // Element references
    const sourceLanguageSelect = document.getElementById('source-language');
    const targetLanguageSelect = document.getElementById('target-language');
    const swapLanguagesBtn = document.getElementById('swap-languages');
    const sourceTextArea = document.getElementById('source-text');
    const translateBtn = document.getElementById('translate-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const translationResult = document.getElementById('translation-result');
    const frameAnalysis = document.getElementById('frame-analysis');
    const toggleFrameInfoBtn = document.getElementById('toggle-frame-info');
    const toggleFrameAnalysisBtn = document.getElementById('toggle-frame-analysis');
    const frameInfoContent = document.getElementById('frame-info');
    const exampleButtons = document.querySelectorAll('.example-btn');
    const frameSelector = document.getElementById('frame-selector');
    const frameIdBadge = document.getElementById('frame-id-badge');
    
    // Frame information elements
    const frameNameElement = document.getElementById('frame-name');
    const frameDescriptionElement = document.getElementById('frame-description');
    const coreElementsList = document.getElementById('core-elements-list');
    const nonCoreElementsList = document.getElementById('non-core-elements-list');
    const lexicalUnitsList = document.getElementById('lexical-units-list');
    
    // Current frame data
    let currentFramePath = '';
    let currentFrameName = '';
    
    // Initialize - load available frames and frame information
    loadAvailableFrames();
    
    // Event listeners
    swapLanguagesBtn.addEventListener('click', swapLanguages);
    translateBtn.addEventListener('click', translateText);
    toggleFrameInfoBtn.addEventListener('click', toggleFrameInfo);
    toggleFrameAnalysisBtn.addEventListener('click', toggleFrameAnalysis);
    
    // Add event listeners for example buttons
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const exampleText = this.textContent;
            const exampleLang = this.getAttribute('data-lang');
            
            sourceTextArea.value = exampleText;
            sourceLanguageSelect.value = exampleLang;
            
            // Automatically set target language to the other language
            targetLanguageSelect.value = exampleLang === 'English' ? 'Japanese' : 'English';
        });
    });
    
    // Function definitions
    
    /**
     * Load available frames
     */
    function loadAvailableFrames() {
        fetch('/api/frames')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    populateFrameSelector(data.data);
                    
                    // Load default frame info if frames are available
                    if (data.data.length > 0) {
                        const defaultFrame = data.data[0];
                        frameSelector.value = defaultFrame.name;
                        loadFrameInfo(defaultFrame.name);
                    } else {
                        console.warn('No frames available');
                    }
                } else {
                    console.error('Failed to load frames:', data.message);
                    alert('Failed to load frames: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error requesting frames:', error);
                alert('Error requesting frames: ' + error.message);
            });
    }
    
    /**
     * Populate frame selector dropdown
     */
    function populateFrameSelector(frames) {
        // Clear existing options
        frameSelector.innerHTML = '';
        
        // Add options for each frame
        frames.forEach(frame => {
            const option = document.createElement('option');
            option.value = frame.name;
            option.textContent = `${frame.name} - ${frame.description}`;
            frameSelector.appendChild(option);
        });
        
        // Add event listener for frame selection
        frameSelector.addEventListener('change', function() {
            const selectedFrameName = this.value;
            if (selectedFrameName) {
                loadFrameInfo(selectedFrameName);
            }
        });
    }
    
    /**
     * Load Frame information
     */
    function loadFrameInfo(frameName) {
        fetch(`/api/frame-info?name=${encodeURIComponent(frameName)}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    currentFramePath = data.data.path;
                    currentFrameName = data.data.frame_name;
                    displayFrameInfo(data.data);
                } else {
                    console.error('Failed to load Frame information:', data.message);
                    alert('Failed to load Frame information: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error requesting Frame information:', error);
                alert('Error requesting Frame information: ' + error.message);
            });
    }
    
    /**
     * Display Frame information
     */
    function displayFrameInfo(frameInfo) {
        // Set Frame name, ID and description
        frameNameElement.textContent = frameInfo.frame_name;
        frameIdBadge.textContent = frameInfo.frame_id;
        frameDescriptionElement.textContent = frameInfo.description;
        
        // Clear lists
        coreElementsList.innerHTML = '';
        nonCoreElementsList.innerHTML = '';
        lexicalUnitsList.innerHTML = '';
        
        // Add core elements
        frameInfo.core_elements.forEach(element => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${element.name}</strong>: ${element.description}`;
            coreElementsList.appendChild(li);
        });
        
        // Add non-core elements
        frameInfo.non_core_elements.forEach(element => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${element.name}</strong>: ${element.description}`;
            nonCoreElementsList.appendChild(li);
        });
        
        // Add lexical units
        frameInfo.lexical_units.forEach(unit => {
            const li = document.createElement('li');
            li.textContent = unit;
            lexicalUnitsList.appendChild(li);
        });
    }
    
    /**
     * Swap source and target languages
     */
    function swapLanguages() {
        const sourceValue = sourceLanguageSelect.value;
        const targetValue = targetLanguageSelect.value;
        
        sourceLanguageSelect.value = targetValue;
        targetLanguageSelect.value = sourceValue;
    }
    
    /**
     * Perform translation
     */
    function translateText() {
        const sourceText = sourceTextArea.value.trim();
        const sourceLanguage = sourceLanguageSelect.value;
        const targetLanguage = targetLanguageSelect.value;
        
        if (!sourceText) {
            alert('Please enter text to translate');
            return;
        }
        
        if (sourceLanguage === targetLanguage) {
            alert('Source and target languages cannot be the same');
            return;
        }
        
        if (!currentFrameName) {
            alert('Please select a frame first');
            return;
        }
        
        // Show loading indicator
        loadingIndicator.style.display = 'flex';
        translateBtn.disabled = true;
        
        // Clear previous results
        translationResult.textContent = '';
        frameAnalysis.innerHTML = '';
        
        // Send translation request
        fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source_text: sourceText,
                source_language: sourceLanguage,
                target_language: targetLanguage,
                frame_name: currentFrameName
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            translateBtn.disabled = false;
            
            if (data.status === 'success') {
                displayTranslationResult(data.data);
            } else {
                console.error('Translation failed:', data.message);
                alert('Translation failed: ' + data.message);
            }
        })
        .catch(error => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            translateBtn.disabled = false;
            
            console.error('Error in translation request:', error);
            alert('Error in translation request: ' + error.message);
        });
    }
    
    /**
     * Display translation result
     */
    function displayTranslationResult(data) {
        // Display translation result
        translationResult.textContent = data.translation;
        
        // Display Frame analysis result
        if (data.frame_analysis) {
            frameAnalysis.innerHTML = formatJSON(data.frame_analysis);
        } else {
            frameAnalysis.textContent = 'No Frame analysis results';
        }
    }
    
    /**
     * Toggle Frame information display/hide
     */
    function toggleFrameInfo() {
        if (frameInfoContent.style.display === 'none') {
            frameInfoContent.style.display = 'grid';
            toggleFrameInfoBtn.textContent = 'Hide';
        } else {
            frameInfoContent.style.display = 'none';
            toggleFrameInfoBtn.textContent = 'Show';
        }
    }
    
    /**
     * Toggle Frame analysis result display/hide
     */
    function toggleFrameAnalysis() {
        if (frameAnalysis.style.display === 'none') {
            frameAnalysis.style.display = 'block';
            toggleFrameAnalysisBtn.textContent = 'Hide';
        } else {
            frameAnalysis.style.display = 'none';
            toggleFrameAnalysisBtn.textContent = 'Show';
        }
    }
    
    /**
     * Format JSON display
     */
    function formatJSON(obj) {
        const jsonString = JSON.stringify(obj, null, 2);
        
        // Add syntax highlighting
        const highlighted = jsonString
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"([^"]+)":/g, '<span class="json-key">"$1"</span>:')
            .replace(/"([^"]*)"/g, '<span class="json-string">"$1"</span>')
            .replace(/\b(\d+)\b/g, '<span class="json-number">$1</span>')
            .replace(/\b(true|false)\b/g, '<span class="json-boolean">$1</span>')
            .replace(/\bnull\b/g, '<span class="json-null">null</span>');
        
        return `<pre>${highlighted}</pre>`;
    }
    
    // Update example sentences based on selected frame
    function updateExampleSentences() {
        // This would ideally fetch examples for the current frame
        // For now, we'll keep the existing examples
    }
    
    // Initialize display/hide state
    frameInfoContent.style.display = 'grid';
    frameAnalysis.style.display = 'block';
});
