<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Security Protocol - Ultra Smooth</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #00f3ff;
            --success: #00ff41;
            --danger: #ff0040;
            --warning: #ffaa00;
            --purple: #a855f7;
            --bg-dark: #0a0e1a;
            --bg-darker: #050811;
            --glass: rgba(255, 255, 255, 0.03);
        }

        @keyframes fade-in {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes scan {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100vh); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px var(--primary); }
            50% { box-shadow: 0 0 40px var(--primary); }
        }

        body {
            background: linear-gradient(135deg, var(--bg-darker) 0%, var(--bg-dark) 100%);
            color: var(--primary);
            font-family: 'Rajdhani', sans-serif;
            overflow-x: hidden;
            min-height: 100vh;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            animation: scan 6s linear infinite;
            z-index: 9999;
            pointer-events: none;
        }

        body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.02) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        header {
            background: rgba(10, 14, 26, 0.9);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--primary);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            animation: glow 3s infinite;
        }

        .header-content {
            max-width: 1800px;
            margin: 0 auto;
            padding: 0 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        h1 {
            font-size: 2em;
            font-weight: 700;
            font-family: 'Share Tech Mono', monospace;
            letter-spacing: 4px;
            text-shadow: 0 0 20px var(--primary);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 20px;
            background: var(--glass);
            border: 1px solid var(--success);
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px var(--success);
        }

        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 30px;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            position: relative;
            z-index: 1;
        }

        .card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 15px;
            padding: 25px;
            animation: fade-in 0.6s ease-out;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: var(--primary);
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 243, 255, 0.2);
        }

        .card-header {
            font-size: 1.4em;
            font-weight: 700;
            color: var(--success);
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        #videoElement {
            width: 100%;
            height: auto;
            border: 2px solid var(--primary);
            border-radius: 10px;
            background: #000;
            box-shadow: 0 5px 30px rgba(0, 243, 255, 0.3);
            display: block;
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px dashed rgba(0, 243, 255, 0.2);
            transition: all 0.3s ease;
        }

        .info-row:hover {
            background: rgba(0, 243, 255, 0.05);
            padding-left: 10px;
            border-left: 2px solid var(--primary);
        }

        .info-label {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.95em;
            font-weight: 500;
        }

        .info-value {
            color: var(--primary);
            font-weight: 700;
            font-size: 1.1em;
            text-shadow: 0 0 10px var(--primary);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }

        .stat-box {
            background: rgba(0, 243, 255, 0.05);
            border: 1px solid var(--primary);
            border-radius: 10px;
            padding: 20px 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .stat-box:hover {
            background: rgba(0, 243, 255, 0.1);
            transform: scale(1.05);
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: 900;
            font-family: 'Share Tech Mono', monospace;
            color: var(--success);
            text-shadow: 0 0 15px var(--success);
            line-height: 1;
        }

        .stat-label {
            font-size: 0.75em;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 8px;
            letter-spacing: 1px;
        }

        .threat-display {
            height: 100px;
            background: var(--bg-darker);
            border: 2px solid var(--success);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .threat-text {
            font-size: 1.6em;
            font-weight: 900;
            font-family: 'Share Tech Mono', monospace;
            color: var(--success);
            text-shadow: 0 0 20px var(--success);
            z-index: 2;
        }

        .threat-display.danger {
            border-color: var(--danger);
            animation: pulse 0.5s infinite;
            background: rgba(255, 0, 64, 0.1);
        }

        .threat-display.danger .threat-text {
            color: var(--danger);
            text-shadow: 0 0 20px var(--danger);
        }

        .threat-display.warning {
            border-color: var(--warning);
            background: rgba(255, 170, 0, 0.1);
        }

        .threat-display.warning .threat-text {
            color: var(--warning);
            text-shadow: 0 0 20px var(--warning);
        }

        .last-capture {
            margin-top: 15px;
            border: 1px solid var(--primary);
            border-radius: 10px;
            overflow: hidden;
        }

        .last-capture img {
            width: 100%;
            height: auto;
            display: block;
        }

        .capture-info {
            padding: 15px;
            background: rgba(0, 243, 255, 0.05);
        }

        .access-history {
            max-height: 400px;
            overflow-y: auto;
            margin-top: 15px;
        }

        .access-history::-webkit-scrollbar {
            width: 8px;
        }

        .access-history::-webkit-scrollbar-track {
            background: var(--bg-darker);
        }

        .access-history::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }

        .history-item {
            display: flex;
            gap: 15px;
            padding: 15px;
            background: rgba(0, 243, 255, 0.03);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 8px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }

        .history-item:hover {
            background: rgba(0, 243, 255, 0.08);
            transform: translateX(5px);
        }

        .history-thumb {
            width: 80px;
            height: 80px;
            border-radius: 5px;
            object-fit: cover;
            border: 1px solid var(--primary);
        }

        .history-details {
            flex: 1;
        }

        .history-name {
            font-size: 1.1em;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 5px;
        }

        .history-time {
            font-size: 0.85em;
            color: rgba(255, 255, 255, 0.6);
        }

        .history-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            margin-top: 5px;
        }

        .history-badge.granted {
            background: rgba(0, 255, 65, 0.2);
            color: var(--success);
            border: 1px solid var(--success);
        }

        .history-badge.denied {
            background: rgba(255, 170, 0, 0.2);
            color: var(--warning);
            border: 1px solid var(--warning);
        }

        .history-badge.weapon {
            background: rgba(255, 0, 64, 0.2);
            color: var(--danger);
            border: 1px solid var(--danger);
        }

        @keyframes slide-in {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .history-item {
            animation: slide-in 0.4s ease-out;
        }

        @media (max-width: 1200px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>⬢ QUANTUM SECURITY PROTOCOL</h1>
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>STREAMING ACTIVE</span>
            </div>
        </div>
    </header>

    <div class="container">
        <!-- Main Video Feed -->
        <div>
            <div class="card">
                <div class="card-header">
                    <span>◉</span> LIVE SURVEILLANCE FEED
                </div>
                <img id="videoElement" src="/video_feed" alt="Loading stream...">
            </div>

            <!-- Access History -->
            <div class="card" style="margin-top: 20px;">
                <div class="card-header">
                    <span>◈</span> ACCESS HISTORY LOG
                </div>
                <div class="access-history" id="accessHistory">
                    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">No access events yet</div>
                </div>
            </div>
        </div>

        <!-- Sidebar -->
        <div class="sidebar">
            <!-- System Status -->
            <div class="card">
                <div class="card-header">
                    <span>⚙</span> SYSTEM STATUS
                </div>
                <div class="info-row">
                    <span class="info-label">CURRENT TIME</span>
                    <span class="info-value" id="currentTime">--:--:--</span>
                </div>
                <div class="info-row">
                    <span class="info-label">SYSTEM UPTIME</span>
                    <span class="info-value" id="uptime">00:00:00</span>
                </div>
                <div class="info-row">
                    <span class="info-label">SYSTEM HEALTH</span>
                    <span class="info-value" id="health">OPTIMAL</span>
                </div>
            </div>

            <!-- Statistics -->
            <div class="card">
                <div class="card-header">
                    <span>◐</span> ANALYTICS
                </div>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-number" id="statGranted">0</div>
                        <div class="stat-label">GRANTED</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="statDenied">0</div>
                        <div class="stat-label">DENIED</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number" id="statWeapons">0</div>
                        <div class="stat-label">THREATS</div>
                    </div>
                </div>
            </div>

            <!-- Last Access -->
            <div class="card">
                <div class="card-header">
                    <span>◪</span> LAST ACCESS EVENT
                </div>
                <div class="info-row">
                    <span class="info-label">PERSON</span>
                    <span class="info-value" id="lastPerson">NONE</span>
                </div>
                <div class="info-row">
                    <span class="info-label">TIME</span>
                    <span class="info-value" id="lastTime">N/A</span>
                </div>
                <div class="last-capture" id="lastCaptureContainer" style="display: none;">
                    <img id="lastCaptureImage" src="" alt="Last capture">
                    <div class="capture-info">
                        <div class="info-value" id="captureEvent">ACCESS EVENT</div>
                    </div>
                </div>
            </div>

            <!-- Threat Status -->
            <div class="card">
                <div class="card-header">
                    <span>⚠</span> THREAT STATUS
                </div>
                <div class="threat-display" id="threatDisplay">
                    <div class="threat-text">SECURE</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let audioContext = null;

        // Initialize audio immediately
        function initAudio() {
            if (!audioContext) {
                try {
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    console.log('[AUDIO] ✅ Audio system initialized');
                } catch (e) {
                    console.warn('[AUDIO] ⚠ Failed to initialize:', e);
                }
            }
        }

        // Try to initialize immediately
        initAudio();

        // Also try on first click
        document.addEventListener('click', initAudio, { once: true });

        // DIFFERENT SOUND EFFECTS

        // Access Granted - Pleasant success chime
        function playAccessGrantedSound() {
            if (!audioContext) return;
            try {
                const osc1 = audioContext.createOscillator();
                const osc2 = audioContext.createOscillator();
                const gain = audioContext.createGain();

                osc1.connect(gain);
                osc2.connect(gain);
                gain.connect(audioContext.destination);

                osc1.type = 'sine';
                osc2.type = 'sine';
                osc1.frequency.setValueAtTime(523, audioContext.currentTime); // C5
                osc2.frequency.setValueAtTime(659, audioContext.currentTime); // E5

                gain.gain.setValueAtTime(0.25, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);

                osc1.start(audioContext.currentTime);
                osc2.start(audioContext.currentTime);
                osc1.stop(audioContext.currentTime + 0.4);
                osc2.stop(audioContext.currentTime + 0.4);

                console.log('[AUDIO] 🔊 Access granted sound played');
            } catch (e) {
                console.error('[AUDIO] Error:', e);
            }
        }

        // Access Denied - Deep buzzer
        function playAccessDeniedSound() {
            if (!audioContext) return;
            try {
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();

                osc.connect(gain);
                gain.connect(audioContext.destination);

                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(220, audioContext.currentTime);
                osc.frequency.linearRampToValueAtTime(110, audioContext.currentTime + 0.5);

                gain.gain.setValueAtTime(0.35, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

                osc.start(audioContext.currentTime);
                osc.stop(audioContext.currentTime + 0.5);

                console.log('[AUDIO] 🔊 Access denied buzzer played');
            } catch (e) {
                console.error('[AUDIO] Error:', e);
            }
        }

        // Weapon Detected - Urgent triple alarm
        function playWeaponDetectedSound() {
            if (!audioContext) return;
            try {
                for (let i = 0; i < 3; i++) {
                    setTimeout(() => {
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();

                        osc.connect(gain);
                        gain.connect(audioContext.destination);

                        osc.type = 'square';
                        osc.frequency.setValueAtTime(880, audioContext.currentTime);

                        gain.gain.setValueAtTime(0.45, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);

                        osc.start(audioContext.currentTime);
                        osc.stop(audioContext.currentTime + 0.2);
                    }, i * 250);
                }

                console.log('[AUDIO] 🚨 WEAPON ALERT SOUND');
            } catch (e) {
                console.error('[AUDIO] Error:', e);
            }
        }

        // Update clock
        function updateClock() {
            const now = new Date();
            document.getElementById('currentTime').textContent = now.toLocaleTimeString();
        }
        setInterval(updateClock, 1000);
        updateClock();

        // Update system data
        function updateSystemData() {
            fetch('/system_data')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('lastPerson').textContent = data.last_person;
                    document.getElementById('lastTime').textContent = data.last_time;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('health').textContent = data.health.toUpperCase();
                    
                    // Update stats
                    updateStat('statGranted', data.stats.granted);
                    updateStat('statDenied', data.stats.denied);
                    updateStat('statWeapons', data.stats.weapons);

                    // Handle events with DIFFERENT sounds
                    const threatDisplay = document.getElementById('threatDisplay');
                    const threatText = threatDisplay.querySelector('.threat-text');

                    if (data.event === 'weapon') {
                        threatDisplay.className = 'threat-display danger';
                        threatText.textContent = '⚠ ARMED THREAT ⚠';
                        playWeaponDetectedSound();
                        setTimeout(() => {
                            threatDisplay.className = 'threat-display';
                            threatText.textContent = 'SECURE';
                        }, 3000);
                    } else if (data.event === 'denied') {
                        threatDisplay.className = 'threat-display warning';
                        threatText.textContent = '⚠ ACCESS DENIED ⚠';
                        playAccessDeniedSound();
                        setTimeout(() => {
                            threatDisplay.className = 'threat-display';
                            threatText.textContent = 'SECURE';
                        }, 2000);
                    } else if (data.event === 'granted') {
                        playAccessGrantedSound();
                    }

                    // Update last capture image
                    if (data.last_image) {
                        document.getElementById('lastCaptureContainer').style.display = 'block';
                        document.getElementById('lastCaptureImage').src = data.last_image;
                        document.getElementById('captureEvent').textContent = data.last_person;
                    }
                })
                .catch(err => console.error('[ERROR] Data fetch failed:', err));
        }

        function updateStat(id, value) {
            const el = document.getElementById(id);
            if (el.textContent != value) {
                el.textContent = value;
                el.style.animation = 'none';
                setTimeout(() => el.style.animation = '', 10);
            }
        }

        // Update access history
        function updateAccessHistory() {
            fetch('/access_history')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('accessHistory');
                    container.innerHTML = '';
                    
                    if (data.history.length === 0) {
                        container.innerHTML = '<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px;">No access events yet</div>';
                        return;
                    }
                    
                    data.history.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'history-item';
                        div.innerHTML = `
                            <img class="history-thumb" src="${item.image}" alt="${item.person}">
                            <div class="history-details">
                                <div class="history-name">${item.person}</div>
                                <div class="history-time">${item.date} at ${item.time}</div>
                                <span class="history-badge ${item.event}">${item.event.toUpperCase()}</span>
                            </div>
                        `;
                        container.appendChild(div);
                    });
                })
                .catch(err => console.error('[ERROR] History fetch failed:', err));
        }

        // Fast polling for responsive system
        setInterval(updateSystemData, 200);
        setInterval(updateAccessHistory, 2000);
        
        // Initial updates
        updateSystemData();
        updateAccessHistory();

        console.log('[SYSTEM] ⚡ Quantum Security Protocol initialized');
        console.log('[SYSTEM] 📹 Pure streaming mode - zero processing lag');
        console.log('[SYSTEM] 🎵 Three different sound effects active');
    </script>
</body>
</html>