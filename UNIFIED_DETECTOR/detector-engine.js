/**
 * UNIFIED DETECTOR ENGINE
 * Consolidates 42 detector tools into one framework
 * Created: 2025-11-25
 */

class UnifiedDetector {
    constructor(containerId = 'app') {
        this.container = document.getElementById(containerId);
        this.currentPattern = null;
        this.selected = new Set();
    }

    // Initialize with pattern data
    init(patterns) {
        this.patterns = patterns;
        this.renderSelector();
    }

    // Render pattern selector dropdown
    renderSelector() {
        const categories = this.groupByCategory();
        const options = Object.entries(categories).map(([cat, items]) => {
            const opts = items.map(p =>
                `<option value="${p.id}">${p.title}</option>`
            ).join('');
            return `<optgroup label="${cat}">${opts}</optgroup>`;
        }).join('');

        this.container.innerHTML = `
            <div class="header">
                <h1>Pattern Detection Suite</h1>
                <p>42 consciousness tools in one</p>
            </div>
            <div class="pattern-selector">
                <select id="patternSelect" onchange="detector.loadPattern(this.value)">
                    <option value="">Select a detector...</option>
                    ${options}
                </select>
            </div>
            <div id="detector-content"></div>
            <footer>
                Pattern Theory | Consciousness Revolution
            </footer>
        `;
    }

    // Group patterns by category
    groupByCategory() {
        const groups = {};
        this.patterns.forEach(p => {
            const cat = p.category || 'Other';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(p);
        });
        return groups;
    }

    // Load a specific pattern
    loadPattern(patternId) {
        this.currentPattern = this.patterns.find(p => p.id === patternId);
        if (!this.currentPattern) return;

        this.selected.clear();
        const content = document.getElementById('detector-content');

        if (this.currentPattern.inputType === 'checkbox') {
            this.renderCheckboxMode(content);
        } else {
            this.renderTextMode(content);
        }
    }

    // Render text input mode
    renderTextMode(content) {
        const p = this.currentPattern;
        content.innerHTML = `
            <div class="header">
                <h1>${p.title}</h1>
                <p>${p.subtitle}</p>
            </div>
            <div class="input-section">
                <textarea class="text-input" id="input" placeholder="${p.placeholder}"></textarea>
                <button class="detect-btn" onclick="detector.detect()">${p.buttonText}</button>
            </div>
            <div class="results" id="results"></div>
        `;
    }

    // Render checkbox mode
    renderCheckboxMode(content) {
        const p = this.currentPattern;
        const checks = p.signs.map((s, i) => `
            <div class="check-item" data-index="${i}" onclick="detector.toggleCheck(${i})">
                <div class="check-box"></div>
                <span class="check-text">${s.text}</span>
            </div>
        `).join('');

        content.innerHTML = `
            <div class="header">
                <h1>${p.title}</h1>
                <p>${p.subtitle}</p>
            </div>
            <div class="check-section">
                <h3>${p.checkPrompt}</h3>
                <div id="checksList">${checks}</div>
                <button class="detect-btn" onclick="detector.analyzeChecks()">${p.buttonText}</button>
            </div>
            <div class="results" id="results"></div>
        `;
    }

    // Toggle checkbox selection
    toggleCheck(index) {
        const item = document.querySelector(`[data-index="${index}"]`);
        if (this.selected.has(index)) {
            this.selected.delete(index);
            item.classList.remove('selected');
        } else {
            this.selected.add(index);
            item.classList.add('selected');
        }
    }

    // Text-based detection
    detect() {
        const text = document.getElementById('input').value.trim();
        if (!text) return;

        const lower = text.toLowerCase();
        const found = [];
        const p = this.currentPattern;

        // Check each tactic
        Object.entries(p.tactics).forEach(([name, data]) => {
            if (data.markers.some(m => lower.includes(m))) {
                found.push({ name, ...data });
            }
        });

        this.renderTextResults(found);
    }

    // Checkbox-based analysis
    analyzeChecks() {
        const p = this.currentPattern;
        let score = 0;
        const warnings = [];

        this.selected.forEach(i => {
            const sign = p.signs[i];
            score += sign.weight || 1;
            warnings.push(sign.text);
        });

        const maxScore = p.signs.reduce((sum, s) => sum + (s.weight || 1), 0);
        const percentage = Math.round((score / maxScore) * 100);

        this.renderCheckResults(percentage, warnings);
    }

    // Render results for text detection
    renderTextResults(found) {
        const p = this.currentPattern;
        let icon, label, desc, labelClass;

        if (found.length === 0) {
            icon = '\u2705';
            label = p.clearLabel || 'NO PATTERNS DETECTED';
            desc = p.clearDesc || 'No manipulation patterns found';
            labelClass = 'clear';
        } else if (found.length <= 2) {
            icon = '\u26A0\uFE0F';
            label = p.warnLabel || 'WARNING SIGNS';
            desc = `${found.length} tactic(s) detected`;
            labelClass = 'warn';
        } else {
            icon = '\u{1F6A8}';
            label = p.dangerLabel || 'HIGH ALERT';
            desc = `${found.length} tactics - serious concern`;
            labelClass = 'danger';
        }

        const responses = found.length > 0
            ? found.map(f => f.response || f.ground).filter(Boolean)
            : [p.defaultResponse || '"Trust your perception"'];

        const realities = this.generateRealities(found);

        document.getElementById('results').innerHTML = `
            <div class="verdict-card">
                <div class="verdict-icon">${icon}</div>
                <div class="verdict-label ${labelClass}">${label}</div>
                <div class="verdict-desc">${desc}</div>
            </div>
            <div class="tactics">
                <h3>Patterns Detected</h3>
                <div id="tacticsList">
                    ${found.length > 0
                        ? found.map(t => `
                            <div class="tactic">
                                <div class="tactic-name">${t.name}</div>
                                <div class="tactic-desc">${t.desc}</div>
                            </div>
                        `).join('')
                        : '<div class="no-tactics">\u2713 No patterns detected</div>'
                    }
                </div>
            </div>
            <div class="responses">
                <h3>How to Respond</h3>
                ${responses.slice(0, 4).map(r =>
                    `<div class="response">${r}</div>`
                ).join('')}
            </div>
            <div class="reality">
                <h4>Reality Check</h4>
                ${realities.map(r =>
                    `<div class="reality-item">\u2022 ${r}</div>`
                ).join('')}
            </div>
        `;

        document.getElementById('results').classList.add('active');
    }

    // Render results for checkbox analysis
    renderCheckResults(percentage, warnings) {
        const p = this.currentPattern;
        let levelClass, label, desc;

        if (percentage <= 20) {
            levelClass = 'low';
            label = 'LOW CONCERN';
            desc = 'Few warning signs detected';
        } else if (percentage <= 50) {
            levelClass = 'medium';
            label = 'MODERATE CONCERN';
            desc = 'Multiple warning signs present';
        } else {
            levelClass = 'high';
            label = 'HIGH ALERT';
            desc = 'Significant pattern detected';
        }

        const guidance = this.generateGuidance(percentage);
        const realities = this.generateRealities([]);

        document.getElementById('results').innerHTML = `
            <div class="verdict-card">
                <div class="verdict-level ${levelClass}">${percentage}%</div>
                <div class="verdict-label">${label}</div>
                <div class="verdict-desc">${desc}</div>
            </div>
            <div class="warning">
                <h3>Warning Signs Present</h3>
                ${warnings.length > 0
                    ? warnings.slice(0, 5).map(w =>
                        `<div class="warning-item">\u26A0\uFE0F ${w}</div>`
                    ).join('')
                    : '<div class="warning-item" style="background: rgba(46, 204, 113, 0.1);">\u2713 No warning signs</div>'
                }
            </div>
            <div class="guidance">
                <h3>What to Do</h3>
                ${guidance.map(g =>
                    `<div class="guide-item">${g}</div>`
                ).join('')}
            </div>
            <div class="reality">
                <h4>Reality Check</h4>
                ${realities.map(r =>
                    `<div class="reality-item">\u2022 ${r}</div>`
                ).join('')}
            </div>
        `;

        document.getElementById('results').classList.add('active');
    }

    // Generate guidance based on severity
    generateGuidance(percentage) {
        const p = this.currentPattern;
        const guidance = [];

        if (percentage > 50 && p.highGuidance) {
            guidance.push(...p.highGuidance);
        } else if (percentage > 20 && p.mediumGuidance) {
            guidance.push(...p.mediumGuidance);
        }

        if (p.defaultGuidance) {
            guidance.push(...p.defaultGuidance);
        }

        return guidance.slice(0, 5);
    }

    // Generate reality checks
    generateRealities(found) {
        const p = this.currentPattern;
        const realities = [...(p.defaultRealities || [
            'Your perception is valid',
            'Trust your instincts',
            'Healthy relationships feel safe'
        ])];

        found.forEach(f => {
            if (f.reality) realities.push(f.reality);
        });

        return realities.slice(0, 4);
    }
}

// Global instance
let detector;

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    detector = new UnifiedDetector('app');
    if (typeof DETECTOR_PATTERNS !== 'undefined') {
        detector.init(DETECTOR_PATTERNS);
    }
});
