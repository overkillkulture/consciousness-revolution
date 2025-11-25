/**
 * UNIFIED DETECTOR PATTERNS
 * Pattern data extracted from 42 detector tools
 * Created: 2025-11-25
 */

const DETECTOR_PATTERNS = [
    // ============================================
    // MANIPULATION DETECTORS
    // ============================================
    {
        id: 'gaslighting',
        category: 'Manipulation',
        title: 'Gaslighting Detector',
        subtitle: 'Identify reality-denying manipulation',
        inputType: 'text',
        placeholder: 'Paste what someone said that made you question your reality...',
        buttonText: 'Analyze for Gaslighting',
        clearLabel: 'NO GASLIGHTING DETECTED',
        clearDesc: 'No obvious reality-denying patterns found',
        warnLabel: 'GASLIGHTING INDICATORS',
        dangerLabel: 'STRONG GASLIGHTING',
        tactics: {
            'Reality Denial': {
                markers: ['that never happened', "didn't happen", "you're imagining", 'making it up', 'in your head'],
                desc: 'Denying events that actually occurred',
                response: '"I know what happened. I was there."'
            },
            'Memory Attack': {
                markers: ["you're forgetting", "don't remember", 'bad memory', "can't remember", 'always forget'],
                desc: 'Attacking your memory to create doubt',
                response: '"My memory is fine. I remember this clearly."'
            },
            'Perception Invalidation': {
                markers: ['too sensitive', 'overreacting', 'crazy', 'paranoid', 'seeing things'],
                desc: 'Making you doubt your perception',
                response: '"My perception is valid. I experienced what I experienced."'
            },
            'Emotion Dismissal': {
                markers: ["shouldn't feel", 'no reason to', 'being dramatic', 'making a big deal', 'not that bad'],
                desc: 'Telling you how to feel about your experience',
                response: '"I decide how I feel about things that happen to me."'
            },
            'Rewriting History': {
                markers: ["that's not what i said", 'what i meant was', 'you misunderstood', 'took it wrong', 'twisted my words'],
                desc: 'Changing the narrative after the fact',
                response: '"I understood exactly what you said."'
            },
            'Blame Reversal': {
                markers: ['your fault', 'you made me', 'because of you', 'look what you', "wouldn't have if you"],
                desc: 'Making you responsible for their actions',
                response: '"You are responsible for your own actions."'
            },
            'Isolation Attempt': {
                markers: ['no one else', 'everyone agrees', 'ask anyone', 'they all think', 'only one who'],
                desc: 'Making you feel alone in your perception',
                response: '"Others\' opinions don\'t change my experience."'
            },
            'Sanity Questioning': {
                markers: ['need help', 'see someone', 'something wrong with you', 'losing it', 'not well'],
                desc: 'Suggesting you\'re mentally unstable',
                response: '"I\'m perfectly capable of assessing my own mental state."'
            }
        },
        defaultRealities: [
            'Your experience is real - you lived it',
            'Confusion after conversations is a red flag',
            'Document incidents in writing',
            'Trust your gut - if something feels wrong, it is'
        ]
    },

    {
        id: 'guilt-trip',
        category: 'Manipulation',
        title: 'Guilt Trip Detector',
        subtitle: 'Identify guilt manipulation in messages',
        inputType: 'text',
        placeholder: 'Paste the message to analyze for guilt manipulation...',
        buttonText: 'Detect Guilt Trips',
        clearLabel: 'NO GUILT TRIPS DETECTED',
        warnLabel: 'MILD GUILT MANIPULATION',
        dangerLabel: 'STRONG GUILT MANIPULATION',
        tactics: {
            "After Everything I've Done": {
                markers: ['after everything', "all i've done", 'i sacrificed', 'i gave up'],
                desc: 'Using past favors to create obligation',
                response: '"I appreciate what you\'ve done, but that doesn\'t obligate me to this specific thing"'
            },
            'Comparison Shame': {
                markers: ['everyone else', 'other people would', 'any good', 'real friend would'],
                desc: 'Comparing you unfavorably to create shame',
                response: '"I make decisions based on what\'s right for me, not comparisons"'
            },
            'Disappointment Play': {
                markers: ['so disappointed', 'let me down', 'thought you were different', 'expected better'],
                desc: 'Expressing disappointment to manipulate',
                response: '"Your disappointment is about your expectations, not my choices"'
            },
            'Hurt Display': {
                markers: ['you hurt me', 'how could you', "can't believe you", 'really hurt'],
                desc: 'Magnifying hurt to create guilt',
                response: '"I\'m sorry you\'re hurt, but I\'m not responsible for your feelings about my boundaries"'
            },
            'Suffering Emphasis': {
                markers: ["i'm suffering", 'in pain', 'struggling', 'hard time', 'going through'],
                desc: 'Emphasizing suffering to obligate help',
                response: '"I care about your wellbeing, but I can\'t always be the solution"'
            },
            'Abandonment Frame': {
                markers: ['abandon', 'leave me', 'walk away', 'give up on', 'not there for me'],
                desc: 'Framing boundaries as abandonment',
                response: '"Setting boundaries isn\'t abandonment - it\'s healthy"'
            },
            'Martyrdom': {
                markers: ["i guess i'll", "don't worry about me", "i'll manage somehow", "if you don't care"],
                desc: 'Playing the martyr to induce guilt',
                response: '"I hear you\'ll manage - I trust you"'
            },
            'Silent Treatment Preview': {
                markers: ["won't bother you", 'leave you alone', 'stop asking', 'keep to myself'],
                desc: 'Threatening withdrawal to manipulate',
                response: '"That\'s your choice. I\'m still here if you want to talk respectfully"'
            }
        },
        defaultRealities: [
            'You are not responsible for other people\'s emotions',
            'Saying "no" is not betrayal - it\'s self-respect',
            'Guilt is a feeling, not a fact',
            'Healthy relationships don\'t require guilt'
        ]
    },

    {
        id: 'love-bombing',
        category: 'Relationship Patterns',
        title: 'Love Bombing Detector',
        subtitle: 'Distinguish genuine affection from manipulation',
        inputType: 'checkbox',
        checkPrompt: 'Check signs that apply (early relationship stage):',
        buttonText: 'Analyze Behavior',
        signs: [
            { text: 'Excessive compliments and flattery very early', weight: 2 },
            { text: 'Says "I love you" or "soulmate" within days/weeks', weight: 3 },
            { text: "Constant texting/calling - upset if you don't respond fast", weight: 2 },
            { text: 'Expensive gifts or grand gestures immediately', weight: 2 },
            { text: 'Wants to be exclusive very quickly', weight: 2 },
            { text: 'Says you\'re "different" from everyone else', weight: 1 },
            { text: 'Future planning (moving in, marriage) very early', weight: 3 },
            { text: 'Gets upset when you spend time with others', weight: 3 },
            { text: 'Tries to meet all your needs so you "need" them', weight: 2 },
            { text: 'Seems too good to be true', weight: 2 },
            { text: 'Your friends/family express concern', weight: 2 },
            { text: 'Dismisses or downplays your boundaries', weight: 3 }
        ],
        highGuidance: [
            "SLOW DOWN - resist the urgency they're creating",
            'Talk to trusted friends/family about their concerns',
            'Watch what happens when you set a boundary'
        ],
        mediumGuidance: [
            'Take things at YOUR pace, not theirs',
            'Notice if intensity decreases when you set limits'
        ],
        defaultGuidance: [
            'Healthy relationships build gradually over time',
            "Pay attention to actions when they don't get what they want",
            'Trust is earned through consistent behavior, not grand gestures'
        ],
        defaultRealities: [
            "Real love is patient - it doesn't rush",
            'Genuine affection respects your boundaries',
            "Healthy partners don't need to overwhelm you",
            'Time reveals character - don\'t skip that'
        ]
    },

    {
        id: 'triangulation',
        category: 'Manipulation',
        title: 'Triangulation Detector',
        subtitle: 'Identify third-party manipulation tactics',
        inputType: 'text',
        placeholder: 'Paste what was said involving another person...',
        buttonText: 'Detect Triangulation',
        tactics: {
            'Jealousy Triggering': {
                markers: ['my ex', 'this other person', 'someone else', 'they were interested', 'flirting with'],
                desc: 'Mentioning others to create jealousy',
                response: '"I notice you\'re bringing up other people. What are you trying to communicate?"'
            },
            'Opinion Weaponizing': {
                markers: ['everyone thinks', 'they all said', 'people are saying', 'others agree', 'told me you'],
                desc: 'Using others\' opinions as weapons',
                response: '"I\'d prefer to discuss this directly, not through third parties"'
            },
            'Comparison Control': {
                markers: ['would never', 'at least they', 'unlike you', 'not like', 'better than you'],
                desc: 'Comparing you unfavorably to others',
                response: '"Comparisons aren\'t helpful. Let\'s focus on us."'
            },
            'Secret Alliance': {
                markers: ['we discussed you', 'we think you', 'agreed that you', 'decided together', 'both noticed'],
                desc: 'Creating alliances against you',
                response: '"I feel excluded when decisions are made about me without me"'
            },
            'Messenger Game': {
                markers: ['they wanted me to tell you', 'passing along', 'they said to ask', 'on their behalf'],
                desc: 'Playing messenger to avoid accountability',
                response: '"If they have concerns, I\'d prefer to hear directly from them"'
            }
        },
        defaultRealities: [
            'Healthy relationships don\'t need third parties for validation',
            'Direct communication builds trust',
            'You deserve to be included in discussions about you',
            'Triangulation is a control tactic, not conflict resolution'
        ]
    },

    {
        id: 'projection',
        category: 'Defense Mechanisms',
        title: 'Projection Detector',
        subtitle: 'Identify when someone projects their issues onto you',
        inputType: 'text',
        placeholder: 'Paste what someone accused you of...',
        buttonText: 'Detect Projection',
        tactics: {
            'Mirror Accusation': {
                markers: ['you always', 'you never', "you're the one who", "you're just like", 'you do the same'],
                desc: 'Accusing you of their exact behavior',
                response: '"I notice this is something you do. Let\'s talk about that."'
            },
            'Motive Assumption': {
                markers: ['you want to', 'you\'re trying to', 'your goal is', 'you think you can', 'you planned'],
                desc: 'Assuming your motives match theirs',
                response: '"You\'re telling me what I\'m thinking. Would you like to ask instead?"'
            },
            'Character Attack': {
                markers: ['you\'re selfish', 'you\'re manipulative', 'you\'re controlling', 'you\'re dishonest', 'you\'re toxic'],
                desc: 'Labeling you with their own traits',
                response: '"That label doesn\'t fit me. I wonder if you\'re describing yourself."'
            },
            'Feeling Displacement': {
                markers: ['you\'re angry', 'you\'re jealous', 'you\'re insecure', 'you\'re afraid', 'you\'re defensive'],
                desc: 'Attributing their emotions to you',
                response: '"Actually, I feel calm. Are you perhaps feeling that way?"'
            }
        },
        defaultRealities: [
            'Their accusations often reveal their own struggles',
            'You know yourself better than they do',
            'Projection is their defense mechanism, not your truth',
            'Consider the source before accepting criticism'
        ]
    },

    {
        id: 'hoovering',
        category: 'Relationship Patterns',
        title: 'Hoovering Detector',
        subtitle: 'Identify attempts to pull you back in',
        inputType: 'text',
        placeholder: 'Paste the message from someone you\'ve distanced from...',
        buttonText: 'Detect Hoovering',
        tactics: {
            'Nostalgia Bait': {
                markers: ['remember when', 'we used to', 'good times', 'miss how', 'think about us'],
                desc: 'Using positive memories to draw you back',
                response: '"I remember, and I also remember why I needed distance."'
            },
            'False Change': {
                markers: ["i've changed", "i'm different now", 'working on myself', 'in therapy', 'realized'],
                desc: 'Claiming transformation without evidence',
                response: '"Change is shown through consistent actions over time, not words."'
            },
            'Emergency Pull': {
                markers: ['something happened', 'need to talk', 'emergency', 'important', 'urgent'],
                desc: 'Creating urgency to bypass boundaries',
                response: '"If it\'s truly urgent, please contact appropriate support."'
            },
            'Guilt Leverage': {
                markers: ['after everything', 'thought we meant more', 'can\'t believe you', 'just disappear'],
                desc: 'Using guilt to override your decision',
                response: '"My decision to step back was about my wellbeing."'
            },
            'Third Party Route': {
                markers: ['your friend said', 'your mom told me', 'ran into', 'heard you'],
                desc: 'Using others to reach you',
                response: '"Please respect my boundary and don\'t involve others."'
            }
        },
        defaultRealities: [
            'You set distance for valid reasons - remember them',
            'Temporary discomfort from boundaries beats long-term harm',
            'Real change is consistent, not just timed with hoovering',
            'You don\'t owe explanations for protecting yourself'
        ]
    },

    {
        id: 'future-faking',
        category: 'Manipulation',
        title: 'Future Faking Detector',
        subtitle: 'Identify empty promises about the future',
        inputType: 'text',
        placeholder: 'Paste the promises they\'ve made...',
        buttonText: 'Detect Future Faking',
        tactics: {
            'Grand Plans': {
                markers: ["we'll", "i'll get", 'going to', 'planning to', 'soon we', 'one day'],
                desc: 'Making big future promises',
                response: '"What concrete steps are happening this week?"'
            },
            'Timeline Shift': {
                markers: ['next month', 'after this', 'once i', 'when things', 'as soon as'],
                desc: 'Pushing promises into vague future',
                response: '"I need specific dates, not indefinite timelines."'
            },
            'Condition Stacking': {
                markers: ['if you', 'when you stop', 'once you', 'after you', 'just need you to'],
                desc: 'Making promises conditional on your behavior',
                response: '"My behavior shouldn\'t determine your follow-through."'
            }
        },
        defaultRealities: [
            'Past behavior predicts future behavior',
            'Real intentions show in current actions',
            'Vague promises keep you waiting indefinitely',
            'Words without timelines are just dreams'
        ]
    },

    {
        id: 'breadcrumbing',
        category: 'Relationship Patterns',
        title: 'Breadcrumbing Detector',
        subtitle: 'Identify minimal effort to keep you interested',
        inputType: 'text',
        placeholder: 'Describe their communication pattern...',
        buttonText: 'Detect Breadcrumbing',
        tactics: {
            'Sporadic Contact': {
                markers: ['out of nowhere', 'randomly texts', 'disappears then', 'only when', 'once in a while'],
                desc: 'Inconsistent, unpredictable contact',
                response: '"I need consistent communication, not random check-ins."'
            },
            'Low Effort Engagement': {
                markers: ['just hey', 'wyd', 'liked my', 'viewed my', 'reacted to'],
                desc: 'Minimal engagement to stay on your radar',
                response: '"A like isn\'t connection. I need actual engagement."'
            },
            'Plans Without Follow-through': {
                markers: ['we should', 'let\'s sometime', 'would be fun', 'sounds good', 'maybe later'],
                desc: 'Suggesting plans but never committing',
                response: '"I\'m done with maybes. Propose a specific time or don\'t."'
            },
            'Attention Reeling': {
                markers: ['thinking of you', 'miss you', 'been meaning to', 'almost called'],
                desc: 'Empty sentiment without action',
                response: '"Thoughts without action don\'t count."'
            }
        },
        defaultRealities: [
            'You deserve consistent attention, not crumbs',
            'Their availability reflects your priority level',
            'Real interest is obvious - you won\'t have to guess',
            'Time invested in breadcrumbers is time wasted'
        ]
    },

    {
        id: 'emotional-blackmail',
        category: 'Manipulation',
        title: 'Emotional Blackmail Detector',
        subtitle: 'Identify FOG tactics (Fear, Obligation, Guilt)',
        inputType: 'text',
        placeholder: 'Paste the threatening or demanding message...',
        buttonText: 'Detect Emotional Blackmail',
        tactics: {
            'Self-Harm Threats': {
                markers: ['hurt myself', 'kill myself', 'won\'t survive', 'nothing to live for', 'end it'],
                desc: 'Threatening self-harm to control you (TAKE SERIOUSLY)',
                response: '"I\'m calling emergency services. This is beyond what I can help with."'
            },
            'Relationship Threats': {
                markers: ['leave you', 'find someone else', 'done with you', 'never speak again', 'tell everyone'],
                desc: 'Threatening relationship consequences',
                response: '"Making threats isn\'t negotiation. I won\'t respond to ultimatums."'
            },
            'Fear Induction': {
                markers: ["you'll regret", 'mark my words', 'wait and see', "you'll be sorry", 'consequences'],
                desc: 'Creating fear of future punishment',
                response: '"I won\'t make decisions based on fear of retaliation."'
            },
            'Obligation Creation': {
                markers: ['owe me', 'you have to', 'it\'s your duty', 'supposed to', 'obligated'],
                desc: 'Creating false obligations',
                response: '"I don\'t owe you control over my decisions."'
            },
            'Victim Positioning': {
                markers: ['look what you did', 'this is your fault', 'you caused this', 'because of you', 'made me'],
                desc: 'Positioning themselves as victim of your choices',
                response: '"You\'re responsible for your own actions and reactions."'
            }
        },
        defaultRealities: [
            'You cannot prevent someone else\'s choices',
            'Threats are not love - they are control',
            'You are not responsible for their reactions to your boundaries',
            'If they threaten self-harm, involve professionals immediately'
        ]
    },

    {
        id: 'stonewalling',
        category: 'Communication Blocks',
        title: 'Stonewalling Analyzer',
        subtitle: 'Identify communication shutdown tactics',
        inputType: 'checkbox',
        checkPrompt: 'Check behaviors you\'ve experienced:',
        buttonText: 'Analyze Pattern',
        signs: [
            { text: 'Refuses to discuss issues', weight: 2 },
            { text: 'Walks away during conversations', weight: 2 },
            { text: 'Gives silent treatment for extended periods', weight: 3 },
            { text: 'Says "I don\'t want to talk about it"', weight: 1 },
            { text: 'Becomes physically unresponsive (blank stare, crossed arms)', weight: 2 },
            { text: 'Changes subject when you raise concerns', weight: 2 },
            { text: 'Pretends not to hear you', weight: 2 },
            { text: 'Uses phone/TV to avoid conversation', weight: 1 },
            { text: 'Leaves the house to avoid discussions', weight: 2 },
            { text: 'Shuts down emotionally for days', weight: 3 }
        ],
        highGuidance: [
            'This pattern prevents any conflict resolution',
            'Consider whether this relationship can meet your needs',
            'Seek couples counseling if they\'re willing'
        ],
        mediumGuidance: [
            'Request time-outs instead of shutdowns',
            'Agree on returning to discuss within 24 hours'
        ],
        defaultGuidance: [
            'You can\'t force someone to communicate',
            'Their withdrawal isn\'t about your worth',
            'Focus on what you can control - your response'
        ],
        defaultRealities: [
            'Stonewalling is emotional withdrawal, not problem-solving',
            'You deserve a partner who engages with you',
            'This pattern often escalates without intervention',
            'Your needs for resolution are valid'
        ]
    },

    {
        id: 'victim-blaming',
        category: 'Defense Mechanisms',
        title: 'Victim Blaming Detector',
        subtitle: 'Identify when blame is shifted to the victim',
        inputType: 'text',
        placeholder: 'Paste what was said to you after you raised an issue...',
        buttonText: 'Detect Victim Blaming',
        tactics: {
            'Behavior Blame': {
                markers: ['if you hadn\'t', 'you shouldn\'t have', 'what did you expect', 'your fault for', 'you provoked'],
                desc: 'Blaming your behavior for their actions',
                response: '"My behavior doesn\'t justify mistreatment."'
            },
            'Character Attack': {
                markers: ['you\'re too', 'that\'s just how you', 'you always', 'typical of you', 'what\'s wrong with you'],
                desc: 'Making it about who you are',
                response: '"Attacking my character doesn\'t address the issue."'
            },
            'Denial of Harm': {
                markers: ['not that bad', 'you\'re overreacting', 'get over it', 'move on', 'let it go'],
                desc: 'Minimizing the impact on you',
                response: '"I get to decide how something affected me."'
            },
            'Hindsight Weaponizing': {
                markers: ['should have known', 'saw it coming', 'what did you think', 'obvious that', 'could have prevented'],
                desc: 'Using hindsight to blame',
                response: '"Hindsight doesn\'t make me responsible for their choices."'
            }
        },
        defaultRealities: [
            'Being victimized is never your fault',
            'Their choices are their responsibility',
            'You don\'t need to defend your right to be upset',
            'Blame-shifting protects the wrongdoer, not you'
        ]
    },

    {
        id: 'toxic-positivity',
        category: 'Emotional Invalidation',
        title: 'Toxic Positivity Detector',
        subtitle: 'Identify invalidating "positive" responses',
        inputType: 'text',
        placeholder: 'Paste the "positive" response you received...',
        buttonText: 'Detect Toxic Positivity',
        tactics: {
            'Emotion Denial': {
                markers: ['just be positive', 'good vibes only', 'don\'t be negative', 'stay positive', 'positive thinking'],
                desc: 'Dismissing negative emotions as wrong',
                response: '"All emotions are valid and serve a purpose."'
            },
            'Silver Lining Force': {
                markers: ['at least', 'could be worse', 'look on the bright side', 'blessing in disguise', 'meant to be'],
                desc: 'Forcing positivity onto real struggles',
                response: '"I need space to process before finding silver linings."'
            },
            'Comparison Minimizing': {
                markers: ['others have it worse', 'be grateful', 'first world problems', 'some people', 'think of those'],
                desc: 'Using comparison to dismiss pain',
                response: '"Comparison doesn\'t diminish my experience."'
            },
            'Spiritual Bypass': {
                markers: ['everything happens for a reason', 'universe has a plan', 'let go and let god', 'manifest', 'karma'],
                desc: 'Using spirituality to avoid addressing pain',
                response: '"I can hold faith and pain at the same time."'
            },
            'Quick Fix Push': {
                markers: ['just', 'simply', 'all you need to do', 'just choose to', 'just decide'],
                desc: 'Oversimplifying complex struggles',
                response: '"If it were that simple, I would have done it already."'
            }
        },
        defaultRealities: [
            'Negative emotions are normal and necessary',
            'Processing pain is healthy - suppressing it isn\'t',
            'You can feel multiple things at once',
            'Real support acknowledges, not dismisses'
        ]
    }
];

// Export for module systems
if (typeof module !== 'undefined') {
    module.exports = DETECTOR_PATTERNS;
}
