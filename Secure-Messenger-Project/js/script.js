(function() {
    const statuses = [
        'Booting secure runtime...',
        'Loading Diffie-Hellman engine...',
        'Hardening AES-256 channel...',
        'Checking SHA-256 integrity...',
        'Opening secure interface...',
        'System ready.'
    ];
    const taglines = [
        'Threat-aware secure messaging simulator',
        'Defense mindset meets hacker perspective',
        'Modern cryptography with real attack stories'
    ];
    let idx = 0;
    const txt  = document.getElementById('splash-status-txt');
    const pct  = document.getElementById('splash-pct');
    const fill = document.getElementById('splash-fill');
    const tagline = document.getElementById('splash-tagline');
    const splash = document.getElementById('splash-screen');
    const codeRain = document.getElementById('splash-code-rain');
    let transitioned = false;

    if (codeRain) {
        const symbols = '01{}[]<>/=+-*#@$%^&';
        const lines = [
            'DH_KEY_EXCHANGE_OK',
            'AES_256_SESSION_LOCK',
            'SHA256_INTEGRITY_PASS',
            'SECURE_CHANNEL_READY',
            'NONCE_ROTATION_ACTIVE',
            'RATCHET_STEP_SYNC'
        ];
        const colCount = 22;
        for (let i = 0; i < colCount; i++) {
            const col = document.createElement('div');
            col.className = 'splash-code-col';
            col.style.left = (i * (100 / colCount) + Math.random() * 1.8) + '%';
            col.style.animationDuration = (5.5 + Math.random() * 4.0) + 's';
            col.style.animationDelay = (-Math.random() * 7.0) + 's';
            let text = '';
            for (let j = 0; j < 20; j++) {
                if (j % 5 === 0) text += lines[Math.floor(Math.random() * lines.length)] + '\n';
                else text += symbols[Math.floor(Math.random() * symbols.length)] + symbols[Math.floor(Math.random() * symbols.length)] + '\n';
            }
            col.textContent = text;
            codeRain.appendChild(col);
        }
    }

    function startEnterTransition() {
        if (!splash || transitioned) return;
        transitioned = true;
        splash.classList.add('entering');
        setTimeout(() => {
            splash.classList.add('hidden');
            setTimeout(() => splash.remove(), 700);
        }, 520);
    }

    const parallaxBg = document.getElementById('parallax-bg');
    const parallaxLayers = parallaxBg?.querySelectorAll('.layer');
    if (parallaxLayers && parallaxLayers.length) {
        window.addEventListener('pointermove', (event) => {
            const x = (event.clientX / window.innerWidth - 0.5) * 22;
            const y = (event.clientY / window.innerHeight - 0.5) * 16;
            parallaxLayers.forEach((layer, idx) => {
                const depth = idx + 2;
                layer.style.transform = `translate3d(${x / depth}px, ${y / depth}px, 0)`;
            });
        });
        window.addEventListener('pointerleave', () => {
            parallaxLayers.forEach((layer) => layer.style.transform = 'translate3d(0,0,0)');
        });
    }

    // Update status text every ~440ms
    const statusInterval = setInterval(() => {
        if (idx < statuses.length - 1) idx++;
        txt.textContent = statuses[idx];
        if (tagline) tagline.textContent = taglines[idx % taglines.length];
    }, 440);

    // Update percentage with easing curve for cinematic feel
    let p = 0;
    const pctInterval = setInterval(() => {
        p = Math.min(p + 1.2, 100);
        const eased = Math.round((1 - Math.pow(1 - p / 100, 2.3)) * 100);
        pct.textContent = Math.min(eased, 100) + '%';
        if (p >= 100) clearInterval(pctInterval);
    }, 24);

    // Dismiss after 3.6s with "open door + zoom in"
    setTimeout(() => {
        clearInterval(statusInterval);
        clearInterval(pctInterval);
        txt.textContent = statuses[statuses.length - 1];
        if (tagline) tagline.textContent = 'Secure Messenger & The Hacker View';
        pct.textContent = '100%';
        startEnterTransition();
    }, 3600);
})();
import { initializeApp }  from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
    import { getDatabase, ref, set, update, onValue }
        from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";

    const firebaseConfig = {
        apiKey:      "AIzaSyCUmMpnWqFP4HUiA_sFXNI4LxnhnPG-m50",
        authDomain:  "mychat-d457f.firebaseapp.com",
        databaseURL: "https://mychat-d457f-default-rtdb.firebaseio.com",
        projectId:   "mychat-d457f"
    };
    const app = initializeApp(firebaseConfig);
    const db  = getDatabase(app);
    const msgRef = ref(db, 'messenger_final');

    /* ---- DH Ratchet ---- */
    const G = 5, P = 23;
    let alicePriv = 6, bobPriv = 15;
    let alicePub  = Math.pow(G, alicePriv) % P;
    let bobPub    = Math.pow(G, bobPriv)   % P;
    let currentRootKey = "", lastSender = "";
    const VIG_KEY = "C";

    /* ---- Friends data ---- */
    let currentFriend = 'Bob';
    const friends = [
        { id:1, name:'Bob',    avatar:'https://i.pinimg.com/1200x/d4/db/31/d4db31705e71ec685625697c3f470b6c.jpg', status:'online',  lastMsg:'Chào bạn!',      time:'5 phút' },
        { id:2, name:'Charlie',avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Charlie&backgroundColor=b6e3f4', status:'offline', lastMsg:'Hẹn gặp lại',   time:'2 giờ'  },
        { id:3, name:'David',  avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=David&backgroundColor=c0aede',  status:'online',  lastMsg:'Đã nhận file',  time:'1 giờ'  },
        { id:4, name:'Eva',    avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Eva&backgroundColor=ffd5dc',    status:'online',  lastMsg:'Cảm ơn bạn!',  time:'30 phút'},
        { id:5, name:'Frank',  avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Frank&backgroundColor=d1f7c4', status:'offline', lastMsg:'Ok để mình xem',time:'3 giờ'  },
        { id:6, name:'Grace',  avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Grace&backgroundColor=ffe4ba', status:'online',  lastMsg:'Mình đi đây',  time:'10 phút'},
        { id:7, name:'Henry',  avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Henry&backgroundColor=c9f0ff', status:'online',  lastMsg:'Chúc ngủ ngon',time:'1 giờ'  },
        { id:8, name:'Ivy',    avatar:'https://api.dicebear.com/7.x/adventurer/svg?seed=Ivy&backgroundColor=f9d4ff',   status:'offline', lastMsg:'Gặp sau nhé',   time:'5 giờ'  }
    ];
    const TEAM_MEMBER_AVATARS = {
        1: 'https://loremflickr.com/240/240/cat?lock=101',
        2: 'data:image/jpeg;base64,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',
        3: 'data:image/jpeg;base64,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',
        4: 'https://loremflickr.com/240/240/cat?lock=104',
        5: 'https://loremflickr.com/240/240/cat?lock=105',
        6: 'https://loremflickr.com/240/240/cat?lock=106'
    };

    function applyTeamMemberAvatars() {
        document.querySelectorAll('.member-avatar[data-member-avatar]').forEach(img => {
            const id = img.getAttribute('data-member-avatar');
            const currentSrc = (img.getAttribute('src') || '').trim();
            const isCustomAvatar =
                currentSrc.startsWith('data:image/') ||
                !/loremflickr\.com\/240\/240\/cat\?lock=/i.test(currentSrc);

            // If a custom src is already pasted in HTML (base64/url), keep it as source of truth.
            if (isCustomAvatar && currentSrc) {
                TEAM_MEMBER_AVATARS[id] = currentSrc;
                return;
            }

            // Fallback to configured map only when current src is still placeholder/default.
            if (TEAM_MEMBER_AVATARS[id]) img.src = TEAM_MEMBER_AVATARS[id];
        });
    }

    // Remove LinkedIn links for non-kept members
    function setupTeamMemberClickHandlers() {
        const keptMembers = ['2', '3', '4']; // Keep LinkedIn for Hồng Đào, Bảo Trân, Minh Hằng
        
        document.querySelectorAll('.member-avatar-frame').forEach(frame => {
            const memberId = frame.querySelector('.member-avatar')?.getAttribute('data-member-avatar');
            
            if (memberId && !keptMembers.includes(memberId)) {
                // Completely remove the <a> tag for non-kept members
                const link = frame.querySelector('a');
                if (link) {
                    // Extract the image and replace the link with just the image
                    const img = link.querySelector('img');
                    if (img) {
                        link.replaceWith(img);
                    }
                }
            }
        });
    }

    function transparentizeLogoBackground() {
        const logo = document.querySelector('.brand-logo');
        if (!logo) return;
        const src = logo.getAttribute('src');
        if (!src) return;
        const img = new Image();
        img.onload = () => {
            try {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                if (!ctx) return;
                ctx.drawImage(img, 0, 0);
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const d = imageData.data;
                const w = canvas.width;
                const h = canvas.height;
                const visited = new Uint8Array(w * h);
                const q = [];
                const isBg = (r, g, b, a) => {
                    const max = Math.max(r, g, b);
                    const min = Math.min(r, g, b);
                    return a > 15 && (max - min) <= 14 && r >= 170 && g >= 170 && b >= 170;
                };
                const pushIfBg = (x, y) => {
                    const i = y * w + x;
                    if (visited[i]) return;
                    const p = i * 4;
                    if (!isBg(d[p], d[p + 1], d[p + 2], d[p + 3])) return;
                    visited[i] = 1;
                    q.push(i);
                };
                for (let x = 0; x < w; x++) { pushIfBg(x, 0); pushIfBg(x, h - 1); }
                for (let y = 0; y < h; y++) { pushIfBg(0, y); pushIfBg(w - 1, y); }
                while (q.length) {
                    const i = q.shift();
                    const p = i * 4;
                    d[p + 3] = 0;
                    const x = i % w;
                    const y = (i / w) | 0;
                    if (x > 0) pushIfBg(x - 1, y);
                    if (x < w - 1) pushIfBg(x + 1, y);
                    if (y > 0) pushIfBg(x, y - 1);
                    if (y < h - 1) pushIfBg(x, y + 1);
                }
                ctx.putImageData(imageData, 0, 0);
                logo.src = canvas.toDataURL('image/png');
            } catch(e) {}
        };
        img.src = src;
    }

    /* ================================================================
    HELPERS
    ================================================================ */
    async function hashImage(file) {
        const buffer = await file.arrayBuffer();
        const wordArr = CryptoJS.lib.WordArray.create(buffer);
        return CryptoJS.SHA256(wordArr).toString();
    }

    function encryptImagePixelByPixel(imageData, sessionKey) {
        const w = imageData.width, h = imageData.height;
        const pixels = imageData.data; // Uint8ClampedArray
        const wordArr = CryptoJS.lib.WordArray.create(pixels);
        const encrypted = CryptoJS.AES.encrypt(wordArr, sessionKey, {
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7,
            iv: CryptoJS.enc.Hex.parse('00000000000000000000000000000000') // Fixed IV for demonstration simplicity
        });
        const cipherWords = encrypted.ciphertext;
        const encryptedBytes = new Uint8Array(cipherWords.sigBytes);
        for (let i = 0; i < cipherWords.sigBytes; i++) {
            encryptedBytes[i] = (cipherWords.words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
        }
        const scrambledData = new Uint8ClampedArray(pixels.length);
        scrambledData.set(encryptedBytes.subarray(0, pixels.length));
        return new ImageData(scrambledData, w, h);
    }

    function decryptImagePixelByPixel(encryptedBase64, w, h, sessionKey) {
        const decrypted = CryptoJS.AES.decrypt(encryptedBase64, sessionKey, {
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7,
            iv: CryptoJS.enc.Hex.parse('00000000000000000000000000000000')
        });
        const decWords = decrypted;
        const decBytes = new Uint8Array(decWords.sigBytes);
        for (let i = 0; i < decWords.sigBytes; i++) {
            decBytes[i] = (decWords.words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
        }
        const recoveredData = new Uint8ClampedArray(w * h * 4);
        recoveredData.set(decBytes.subarray(0, w * h * 4));
        return new ImageData(recoveredData, w, h);
    }

    function displayScrambledImageInBlackbox(imageData, label = "SCRAMBLED IMAGE", info = "") {
        const log = document.getElementById('processLog');
        if (!log) return;
        
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        const timeStr = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit', second:'2-digit' });
        
        const canvas = document.createElement('canvas');
        canvas.width = imageData.width;
        canvas.height = imageData.height;
        canvas.style.maxWidth = "100%";
        canvas.style.height = "auto";
        canvas.style.marginTop = "10px";
        canvas.style.borderRadius = "8px";
        canvas.style.border = "1px solid rgba(255,255,255,0.2)";
        const ctx = canvas.getContext('2d');
        ctx.putImageData(imageData, 0, 0);

        entry.innerHTML = `
            <div class="log-header">
                <span class="log-badge"><i class="fas fa-microchip"></i> ${label}</span>
                <span style="color:#75b9e6;font-size:.68rem;"><i class="far fa-clock"></i> ${timeStr}</span>
            </div>
            <div class="log-row">
                <span class="log-value" style="font-size:0.75rem; color:#9ec3e3;">${info}</span>
            </div>
        `;
        entry.appendChild(canvas);
        log.prepend(entry);
    }
    function computeRoot(myPriv, otherPub) {
        const shared = Math.pow(otherPub, myPriv) % P;
        return CryptoJS.SHA256(shared.toString()).toString().substring(0, 16);
    }

    function vigenere(text, key, encrypt = true) {
        text = text.toUpperCase(); key = key.toUpperCase();
        let res = "";
        for (let i = 0; i < text.length; i++) {
            const p = text.charCodeAt(i);
            if (p >= 65 && p <= 90) {
                const pIdx = p - 65, kIdx = key.charCodeAt(i % key.length) - 65;
                const newIdx = encrypt ? (pIdx + kIdx) % 26 : (pIdx - kIdx + 26) % 26;
                res += String.fromCharCode(newIdx + 65);
            } else res += text[i];
        }
        return res;
    }

    function updateRootKeyUI() {
        const el = document.getElementById('aliceKey');
        if (el) el.textContent = currentRootKey || '--------------';
    }

    function loadAccountInfo() {
        const n = document.getElementById('inputName');
        const e = document.getElementById('inputEmail');
        if (n) n.value = localStorage.getItem('accountName')   || 'Alice';
        if (e) e.value = localStorage.getItem('accountEmail')  || 'alice@example.com';
    }
    const statusPill = document.querySelector('.status-pill span[data-i18n="online"]');
    /* ================================================================
    TYPING INDICATOR — Alice → Bob's column (messenger dots)
    ================================================================ */
    let aliceTypingTimer = null;

    function showAliceTyping() {
        const bubble = document.getElementById('aliceTypingBubble');
        const label  = document.getElementById('aliceTypingLabel');
        if (!bubble) return;

        // Move typing bubble to bottom of bobOutput
        const bobOut = document.getElementById('bobOutput');
        if (bobOut) {
            bobOut.appendChild(bubble);
            if (label) bobOut.appendChild(label);
        }

        bubble.classList.add('show');
        if (label) label.classList.add('show');
        if (bobOut) bobOut.scrollTop = bobOut.scrollHeight;
    }

    function hideAliceTyping() {
        const bubble = document.getElementById('aliceTypingBubble');
        const label  = document.getElementById('aliceTypingLabel');
        bubble && bubble.classList.remove('show');
        label  && label.classList.remove('show');
    }

    document.getElementById('aliceInput').addEventListener('input', () => {
        showAliceTyping();
        clearTimeout(aliceTypingTimer);
        aliceTypingTimer = setTimeout(hideAliceTyping, 1800);
    });
    document.getElementById('aliceInput').addEventListener('blur', () => {
        clearTimeout(aliceTypingTimer);
        hideAliceTyping();
    });

    /* ================================================================
    TYPING INDICATOR — Bob → Alice's column (messenger dots)
    ================================================================ */
    let bobTypingTimer = null;

    function showBobTyping() {
        const bubble = document.getElementById('bobTypingBubble');
        const label  = document.getElementById('bobTypingLabel');
        if (!bubble) return;

        const aliceOut = document.getElementById('aliceOutput');
        if (aliceOut) {
            aliceOut.appendChild(bubble);
            if (label) aliceOut.appendChild(label);
        }

        bubble.classList.add('show');
        if (label) label.classList.add('show');
        if (aliceOut) aliceOut.scrollTop = aliceOut.scrollHeight;
    }

    function hideBobTyping() {
        const bubble = document.getElementById('bobTypingBubble');
        const label  = document.getElementById('bobTypingLabel');
        bubble && bubble.classList.remove('show');
        label  && label.classList.remove('show');
    }

    document.getElementById('bobInput').addEventListener('input', () => {
        showBobTyping();
        clearTimeout(bobTypingTimer);
        bobTypingTimer = setTimeout(hideBobTyping, 1800);
    });
    document.getElementById('bobInput').addEventListener('blur', () => {
        clearTimeout(bobTypingTimer);
        hideBobTyping();
    });

    /* ================================================================
    SEEN INDICATOR — Bob hovers on his column → show in Alice's area
    ================================================================ */
    const bobColumn = document.querySelector('.column.bob');
    const seenEl    = document.getElementById('aliceSeenIndicator');

    function showSeen() {
        if (!seenEl) return;
        // Move seen indicator below the last .bubble.self in aliceOutput
        const aliceOut = document.getElementById('aliceOutput');
        if (!aliceOut) return;
        aliceOut.appendChild(seenEl);       // re-append to keep at bottom
        aliceOut.scrollTop = aliceOut.scrollHeight;
        // small delay so it renders after append
        requestAnimationFrame(() => seenEl.classList.add('visible'));
    }
    function hideSeen() {
        seenEl && seenEl.classList.remove('visible');
    }

    if (bobColumn) {
        bobColumn.addEventListener('mouseenter', showSeen);
        // Seen stays visible once triggered — no mouseleave hide
    }

    /* ================================================================
    SEEN INDICATOR — Alice hovers on her column → show in Bob's area
    ================================================================ */
    const aliceColumn  = document.querySelector('.column.alice');
    const bobSeenEl    = document.getElementById('bobSeenIndicator');

    function showBobSeen() {
        if (!bobSeenEl) return;
        const bobOut = document.getElementById('bobOutput');
        if (!bobOut) return;
        bobOut.appendChild(bobSeenEl);
        bobOut.scrollTop = bobOut.scrollHeight;
        requestAnimationFrame(() => bobSeenEl.classList.add('visible'));
    }

    if (aliceColumn) {
        aliceColumn.addEventListener('mouseenter', showBobSeen);
    }

    /* ================================================================
    BOB TYPING INDICATOR (text line below Bob's input)
    ================================================================ */
    const bobTypingTimers = {};

    function setupTypingText(sender, inputId) {
        const input = document.getElementById(inputId);
        const el    = document.getElementById(sender.toLowerCase() + 'Typing');
        if (!input || !el) return;
        input.addEventListener('input', () => {
            el.textContent = sender + t('typerIsTyping');
            el.style.opacity = '1';
            clearTimeout(bobTypingTimers[sender]);
            bobTypingTimers[sender] = setTimeout(() => {
                el.style.opacity = '0';
                setTimeout(() => { el.textContent = ''; }, 200);
            }, 1400);
        });
        input.addEventListener('blur', () => { el.style.opacity = '0'; });
    }
    setupTypingText('Bob',    'bobInput');
    setupTypingText('Friend', 'friendInput');

    /* ================================================================
    TOGGLE CONSOLE
    ================================================================ */
    window.toggleBlackbox = function() {
        const hidden = document.body.classList.toggle('hide-process');
        const btn = document.getElementById('toggleBlackboxBtn').querySelector('[data-i18n]');
        if (btn) {
            btn.setAttribute('data-i18n', hidden ? 'showConsole' : 'hideConsole');
            btn.textContent = hidden ? t('showConsole') : t('hideConsole');
        }
    };

    /* ================================================================
    ACCORDION TOGGLE (removed - using native <details>)
    ================================================================ */

    /* ================================================================
    PAGE SWITCH
    ================================================================ */
    function getAliceSession() {
        const name = (localStorage.getItem('alice_login_name') || '').trim();
        const email = (localStorage.getItem('alice_login_email') || '').trim();
        return { name, email, loggedIn: !!(name && email) };
    }

    function updateAuthUI() {
        const authBtn = document.getElementById('authToggleBtn');
        const authLabel = document.getElementById('authLabel');
        if (!authBtn || !authLabel) return;
        const session = getAliceSession();
        const isEn = currentLang === 'en';
        const icon = authBtn.querySelector('i');
        if (session.loggedIn) {
            authLabel.textContent = isEn ? 'Logout' : 'Đăng xuất';
            if (icon) icon.className = 'fas fa-right-from-bracket';
            authBtn.title = `Alice: ${session.name} (${session.email})`;
        } else {
            authLabel.textContent = isEn ? 'Login' : 'Đăng nhập';
            if (icon) icon.className = 'fas fa-right-to-bracket';
            authBtn.title = isEn ? 'Login to Alice account' : 'Đăng nhập tài khoản Alice';
        }
    }

    window.openAuthModal = function() {
        const modal = document.getElementById('authModal');
        if (!modal) return;
        const session = getAliceSession();
        const nameInput = document.getElementById('authName');
        const emailInput = document.getElementById('authEmail');
        if (nameInput) nameInput.value = session.name || localStorage.getItem('accountName') || '';
        if (emailInput) emailInput.value = session.email || localStorage.getItem('accountEmail') || 'alice@example.com';
        modal.classList.add('show');
        if (nameInput) nameInput.focus();
    };

    window.closeAuthModal = function() {
        const modal = document.getElementById('authModal');
        if (modal) modal.classList.remove('show');
    };
    document.getElementById('authModal')?.addEventListener('click', (e) => {
        if (e.target.id === 'authModal' && window.innerWidth < 961) closeAuthModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAuthModal();
            document.getElementById('xssModal')?.classList.remove('show');
        }
    });

// 1. Mở/Đóng Modal
window.openAccountModal = function() {
    document.getElementById('accountModal').style.display = 'flex';
    // Tải thông tin hiện tại vào ô nhập
    document.getElementById('inputName').value = localStorage.getItem('accountName') || 'Alice';
    document.getElementById('inputEmail').value = localStorage.getItem('accountEmail') || 'alice@example.com';
};

window.closeAccountModal = function() {
    document.getElementById('accountModal').style.display = 'none';
};

// 2. Xử lý ảnh Avatar (Chuyển sang Base64 để lưu vào localStorage)
document.getElementById('avatarInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const base64 = event.target.result;
            document.getElementById('avatarPreview').src = base64;
            localStorage.setItem('accountAvatar', base64);
        };
        reader.readAsDataURL(file);
    }
});

// Hàm openAccountModal và closeAccountModal không trùng lapped

    document.getElementById('avatarInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const base64 = event.target.result;
                document.getElementById('avatarPreview').src = base64;
                localStorage.setItem('accountAvatar', base64);
            };
            reader.readAsDataURL(file);
        }
    });

    window.saveAccountInfo = function() {
        const n = document.getElementById('inputName').value.trim() || 'Alice';
        const e = document.getElementById('inputEmail').value.trim() || 'alice@example.com';
        
        // 1. Lưu vào bộ nhớ cục bộ
        localStorage.setItem('accountName', n);
        localStorage.setItem('accountEmail', e);

        // 2. ĐỔI TÊN TẬN GỐC TRONG HỆ THỐNG NGÔN NGỮ (Chống bị ghi đè lại)
        if (typeof i18nStrings !== 'undefined') {
            i18nStrings.vi.aliceName = n + " (Bạn)";
            i18nStrings.en.aliceName = n + " (You)";
        }

        // 3. Quét toàn bộ trang web và ép các chữ "Alice (Bạn)" hiện tại thành tên mới
        document.querySelectorAll('[data-i18n="aliceName"]').forEach(el => {
            el.textContent = n + " (Bạn)";
        });

        // Đóng cửa sổ cài đặt
        document.getElementById('accountModal').style.display = 'none';
        
        // Hiện thông báo thành công
        showToast(t('updateNameSuccess'));
    };

    window.submitAliceLogin = function() {
        const name = (document.getElementById('authName')?.value || '').trim();
        const email = (document.getElementById('authEmail')?.value || '').trim();
        
        // Lấy tên và email mới nhất đã lưu (nếu đã đổi trong phần Account)
        const savedName = localStorage.getItem('accountName') || 'Alice';
        const savedEmail = localStorage.getItem('accountEmail') || 'alice@example.com';

        // Kiểm tra xem người dùng có gõ đúng tên mới hoặc email mới không
        if (name !== savedName || email !== savedEmail) {
            showToast('⚠️ Tên hoặc email không đúng với tài khoản hiện tại!');
            return;
        }

        const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        if (!name || !email || !emailOk) {
            showToast('⚠️ ' + t('invalidEmail'));
            return;
        }
        
        localStorage.setItem('alice_login_name', name);
        localStorage.setItem('alice_login_email', email);
        closeAuthModal();
        showToast('✅ ' + t('loginSuccess') + name);
        updateAuthUI();
    };

    window.toggleAliceAuth = function() {
        const session = getAliceSession();
        if (session.loggedIn) {
            if (!confirm(t('logoutConfirm'))) return;
            localStorage.removeItem('alice_login_name');
            localStorage.removeItem('alice_login_email');
            showToast(t('logoutSuccess'));
            updateAuthUI();
            switchPage('project');
            return;
        }
        openAuthModal();
    };

    window.switchPage = function(page, event) {
        if (event) event.preventDefault();
        const session = getAliceSession();
        if (page !== 'team' && page !== 'project' && !session.loggedIn) {
            showToast('🔐 ' + t('loginToView'));
            page = 'project';
        }
        document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
        const target = document.getElementById(`page-${page}`);
        if (target) {
            target.style.display = 'block';
            target.classList.remove('page-animate');
            void target.offsetWidth;
            target.classList.add('page-animate');
        }
        
        // Update active states for all navigation links
        document.querySelectorAll('.header-left a, .app-nav a')
            .forEach(a => a.classList.toggle('active', a.dataset.page === page));
            
        if (page === 'account') { loadAccountInfo(); updateRootKeyUI(); }
        if (page === 'friends') { renderFriendsList(); loadFriendMessages(currentFriend); }
    };

    window.saveAccountInfo = function() {
        localStorage.setItem('accountName',   (document.getElementById('inputName').value.trim()   || 'Alice'));
        localStorage.setItem('accountEmail',  (document.getElementById('inputEmail').value.trim()  || 'alice@example.com'));
        loadAccountInfo();
        // Update display name/email in header
        const n = document.getElementById('inputName').value.trim() || 'Alice';
        const e = document.getElementById('inputEmail').value.trim() || 'alice@example.com';
        const dn = document.getElementById('accDisplayName');
        const de = document.getElementById('accDisplayEmail');
        if (dn) dn.innerHTML = `<i class="fas fa-cloud"></i> ${n}`;
        if (de) de.textContent = e;
        // Show toast instead of alert
        showToast(t('accountSaveSuccess'));
    };

    /* ================================================================
    FRIENDS
    ================================================================ */
    function renderFriendsList(filter = '') {
        const list = document.getElementById('friendsList');
        if (!list) return;
        const filtered = filter
            ? friends.filter(f => f.name.toLowerCase().includes(filter))
            : friends;
        list.innerHTML = filtered.map(f => `
            <div class="friend-item ${f.name === currentFriend ? 'active' : ''}"
                onclick="selectFriend('${f.name}')">
                <button class="friend-delete-btn" onclick="deleteFriendMessages('${f.name}', event)" data-friend-name="${f.name}">
                    <i class="fas fa-trash"></i>
                </button>
                <img src="${f.avatar}" class="friend-avatar" alt="${f.name}">
                <div class="friend-info">
                    <div class="friend-name">
                        ${f.name}
                        <span class="status-dot" style="${f.status !== 'online' ? 'background:#888;box-shadow:none;animation:none;' : ''}"></span>
                    </div>
                    <div class="friend-preview">${f.lastMsg}</div>
                </div>
                <div class="friend-time">${f.time}</div>
            </div>`).join('');

        // Set friend delete button titles dynamically for i18n
        document.querySelectorAll('.friend-delete-btn[data-friend-name]').forEach(btn => {
            const friendName = btn.getAttribute('data-friend-name');
            btn.title = t('deleteFriendMessagesTitle') + friendName;
        });

        const search = document.getElementById('friendSearch');
        if (search && !search.dataset.bound) {
            search.dataset.bound = '1';
            search.addEventListener('input', e => renderFriendsList(e.target.value.toLowerCase()));
        }
    }

    window.selectFriend = function(name) {
        currentFriend = name;
        renderFriendsList();
        const f = friends.find(x => x.name === name);
        if (f) {
            document.getElementById('friendChatHeader').innerHTML = `
                <img src="${f.avatar}" class="avatar" alt="${name}">
                <div class="user-info">
                    <h4><i class="fas fa-user-astronaut"></i> ${name}</h4>
                    <span class="status-pill">
                        <span class="status-dot" style="${f.status !== 'online' ? 'background:#888;box-shadow:none;animation:none;' : ''}"></span>
                        ${f.status === 'online' ? 'Online' : 'Offline'}
                    </span>
                </div>`;
        }
        loadFriendMessages(name);
    };
    window.deleteFriendMessages = function(name, event) {
        if (event) event.stopPropagation();
        if (!confirm(t('deleteAllMessagesConfirm') + ` ${name}?`)) return;
        clearHistory(name);
        const f = friends.find(x => x.name === name);
        if (f) {
            f.lastMsg = t('noMessages');
            f.time = '--';
        }
        if (currentFriend === name) loadFriendMessages(name);
        renderFriendsList();
        showToast(`🧹 ${t('deleteAllChatSuccess')}`);
    };

    /* ================================================================
    CHAT HISTORY — localStorage per friend
    ================================================================ */
    function getChatKey(name) { return `chat_history_${name}`; }

    function loadHistory(name) {
        try { return JSON.parse(localStorage.getItem(getChatKey(name))) || []; }
        catch(e) { return []; }
    }

    function saveHistory(name, history) {
        try { localStorage.setItem(getChatKey(name), JSON.stringify(history)); } catch(e) {}
    }

    function addToHistory(name, msg) {
        const h = loadHistory(name);
        h.push(msg);
        saveHistory(name, h);
        // Update preview in friends list
        const f = friends.find(x => x.name === name);
        if (f) {
            f.lastMsg = msg.type === 'image' ? '📷 Hình ảnh' : msg.text;
            f.time = 'Vừa xong';
        }
        renderFriendsList();
    }

    function clearHistory(name) {
        localStorage.removeItem(getChatKey(name));
        loadFriendMessages(name);
    }

    function loadFriendMessages(name) {
        const area = document.getElementById('friendMessageArea');
        if (!area) return;
        area.innerHTML = '';

        const history = loadHistory(name);
        if (history.length === 0) {
            // Default greeting messages
            const defaults = [
                { type:'text', text:`${t('greetingDefault')} ${name}`, sender:'friend', time: Date.now()-60000 },
                { type:'text', text:`${t('greetingResponse1')} ${name}, mình khoẻ!`, sender:'self',   time: Date.now()-30000 }
            ];
            saveHistory(name, defaults);
            defaults.forEach(m => renderHistoryItem('friendMessageArea', m));
        } else {
            history.forEach(m => renderHistoryItem('friendMessageArea', m));
        }

        // Add clear history button
        let clearBar = document.getElementById('clearHistoryBar');
        if (!clearBar) {
            clearBar = document.createElement('div');
            clearBar.id = 'clearHistoryBar';
            clearBar.style.cssText = `display:flex;justify-content:center;padding:.5rem;border-top:1px solid rgba(176,28,45,.12);background:rgba(255,255,255,.9);flex-shrink:0;`;
            clearBar.innerHTML = `<button onclick="clearFriendHistory()" style="background:none;border:1px solid rgba(176,28,45,.35);color:rgba(176,28,45,.8);font-family:Quicksand,sans-serif;font-size:.72rem;font-weight:600;padding:.3rem 1rem;border-radius:30px;cursor:pointer;display:flex;align-items:center;gap:.3rem;transition:background .15s;" onmouseover="this.style.background='rgba(176,28,45,.08)'" onmouseout="this.style.background='none'"><i class="fas fa-trash-alt"></i> Xoá lịch sử chat</button>`;
            const chatContainer = document.getElementById('friendChatContainer');
            if (chatContainer) chatContainer.appendChild(clearBar);
        }

        area.scrollTop = area.scrollHeight;
    }

    window.clearFriendHistory = function() {
        if (!confirm(t('deleteAllMessagesConfirm') + ` ${currentFriend}?`)) return;
    };

    function renderHistoryItem(containerId, m) {
        if (m.type === 'image') {
            appendImageBubble(containerId, m.src, m.sender);
        } else {
            appendBubble(containerId, m.text, m.sender, {});
        }
    }

    window.sendFriendMessage = function() {
        const inp = document.getElementById('friendInput');
        const msg = inp.value.trim();
        const mode = document.querySelector('input[name="modeFriend"]:checked')?.value || 'AES';

        // Send pending images: Base64 -> encrypt -> decrypt -> render
        if (pendingImages.friend && pendingImages.friend.length > 0) {
            pendingImages.friend.forEach(img => {
                const ts = Date.now();
                const payload = makeImagePayload(img.mime, img.base64);
                const enc = encryptPayloadForMode(payload, mode, ts);
                const dec = decryptPayloadForMode({ m: mode, c: enc.cipher, sk: enc.sessionKey, h: enc.hash, ts });
                const parsed = parseImagePayload(dec.payload);
                if (parsed) {
                    appendImageBubble('friendMessageArea', parsed.src, 'self');
                    addToHistory(currentFriend, { type:'image', src: parsed.src, sender:'self', time: ts });
                }
            });
            pendingImages.friend = [];
            const strip = document.getElementById('friendImgStrip');
            if (strip) { strip.innerHTML = ''; strip.classList.remove('has-images'); }
        }

        if (!msg) return;
        appendBubble('friendMessageArea', msg, 'self', {});
        addToHistory(currentFriend, { type:'text', text:msg, sender:'self', time: Date.now() });
        inp.value = '';

        setTimeout(() => {
            const replies = t('friendReplies');
            const reply = replies[Math.floor(Math.random() * replies.length)];
            appendBubble('friendMessageArea', reply, 'friend', {});
            addToHistory(currentFriend, { type:'text', text:reply, sender:'friend', time: Date.now() });
        }, 900);
    };

    /* ================================================================
    IMAGE SEND — Base64 -> encrypt -> decrypt -> render
    ================================================================ */
    const pendingImages = { alice: [], bob: [], friend: [] };
    const IMG_PREFIX = "__IMG__";

    function splitDataUrl(dataUrl) {
        const m = /^data:(.*?);base64,(.*)$/.exec(dataUrl || "");
        if (!m) return null;
        return { mime: m[1], base64: m[2] };
    }

    function makeImagePayload(mime, base64) {
        return `${IMG_PREFIX}${mime}|${base64}`;
    }

    function parseImagePayload(payload) {
        if (!payload || !payload.startsWith(IMG_PREFIX)) return null;
        const body = payload.substring(IMG_PREFIX.length);
        const sep = body.indexOf("|");
        if (sep < 0) return null;
        const mime = body.substring(0, sep);
        const base64 = body.substring(sep + 1);
        if (!mime || !base64) return null;
        return { mime, base64, src: `data:${mime};base64,${base64}` };
    }

    window.handleImgSelect = function(who, input) {
        const strip = document.getElementById(who + 'ImgStrip');
        const files = Array.from(input.files);
        files.forEach(file => {
            const reader = new FileReader();
            reader.onload = e => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let w = img.width, h = img.height;
                    const max = 400;
                    if (w > max || h > max) {
                        if (w > h) { h = Math.round(h * max / w); w = max; }
                        else { w = Math.round(w * max / h); h = max; }
                    }
                    canvas.width = w; canvas.height = h;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, w, h);
                    const imageData = ctx.getImageData(0, 0, w, h);
                    
                    pendingImages[who].push({ 
                        file, 
                        imageData, 
                        preview: canvas.toDataURL('image/png'),
                        width: w, 
                        height: h 
                    });

                    // Add thumb preview
                    const thumb = document.createElement('div');
                    thumb.className = 'img-preview-thumb';
                    const idx = pendingImages[who].length - 1;
                    thumb.innerHTML = `<img src="${canvas.toDataURL('image/png')}">
                        <button class="remove-img" onclick="removeImg('${who}',${idx},this)">✕</button>`;
                    strip.appendChild(thumb);
                    strip.classList.add('has-images');
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
        input.value = '';
    };

    window.removeImg = function(who, idx, btn) {
        pendingImages[who].splice(idx, 1);
        btn.parentElement.remove();
        const strip = document.getElementById(who + 'ImgStrip');
        if (pendingImages[who].length === 0) strip.classList.remove('has-images');
        // Re-index remaining remove buttons
        strip.querySelectorAll('.remove-img').forEach((b, i) => {
            b.setAttribute('onclick', `removeImg('${who}',${i},this)`);
        });
    };

    function flushImages(who, outputId, type) {
        pendingImages[who].forEach(img => {
            appendImageBubble(outputId, img.preview || `data:${img.mime};base64,${img.base64}`, type);
        });
        pendingImages[who] = [];
        const strip = document.getElementById(who + 'ImgStrip');
        if (strip) { strip.innerHTML = ''; strip.classList.remove('has-images'); }
    }

    function appendImageBubble(containerId, src, type) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const div = document.createElement('div');
        div.className = `bubble ${type}`;
        const time = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });
        div.innerHTML = `<img class="bubble-img" src="${src}" onclick="this.style.maxHeight=this.style.maxHeight?'':'none'">
            <span class="timestamp"><i class="far fa-clock"></i> ${time}</span>
            <div class="reactions"></div>
            <div class="quick-reactions"></div>`;
        const typingBubble = container.querySelector('.typing-bubble');
        const seenInd      = container.querySelector('.seen-indicator');
        if (typingBubble) container.insertBefore(div, typingBubble);
        else if (seenInd) container.insertBefore(div, seenInd);
        else container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    }

    function ensureRootKey() {
        if (!currentRootKey) {
            currentRootKey = computeRoot(alicePriv, bobPub);
            updateRootKeyUI();
        }
    }

    function encryptPayloadForMode(payload, mode, ts) {
        ensureRootKey();
        const sessionKey = mode === "AES"
            ? CryptoJS.HmacSHA256(ts.toString(), currentRootKey).toString().substring(0, 16)
            : VIG_KEY;
        const rawData = payload + "|" + ts;
        const hash = mode === "AES"
            ? CryptoJS.HmacSHA256(rawData, sessionKey).toString()
            : CryptoJS.SHA256(rawData).toString();
        const cipher = mode === "AES"
            ? CryptoJS.AES.encrypt(rawData + "|" + hash, sessionKey).toString()
            : vigenere(rawData, VIG_KEY, true);
        return { sessionKey, hash, cipher };
    }

    function decryptPayloadForMode(packet) {
        let payload = "";
        let ok = false;
        if (packet.m === "AES") {
            const bytes = CryptoJS.AES.decrypt(packet.c, packet.sk);
            const full = bytes.toString(CryptoJS.enc.Utf8);
            const lastPipe = full.lastIndexOf("|");
            const rest = full.substring(0, lastPipe);
            const secondLastPipe = rest.lastIndexOf("|");
            payload = rest.substring(0, secondLastPipe);
            const rawCheck = payload + "|" + packet.ts;
            const checkH = CryptoJS.HmacSHA256(rawCheck, packet.sk).toString();
            ok = checkH === packet.h;
        } else {
            const vigFull = vigenere(packet.c, VIG_KEY, false);
            const lastPipe = vigFull.lastIndexOf("|");
            payload = vigFull.substring(0, lastPipe > 0 ? vigFull.lastIndexOf("|", lastPipe - 1) : lastPipe);
            if (!payload) payload = vigFull.split("|")[0];
            ok = true;
        }
        return { payload, ok };
    }

    /* ================================================================
    SEND DATA (Home page)
    ================================================================ */
    window.sendData = async function(sender) {
        const inputId  = sender === 'Alice' ? 'aliceInput' : 'bobInput';
        const modeName = sender === 'Alice' ? 'modeA'      : 'modeB';
        const who      = sender === 'Alice' ? 'alice'      : 'bob';
        const outId    = sender === 'Alice' ? 'aliceOutput': 'bobOutput';
        const peerOut  = sender === 'Alice' ? 'bobOutput'  : 'aliceOutput';
        const msg  = document.getElementById(inputId).value;
        const mode = document.querySelector(`input[name="${modeName}"]:checked`).value;

        const hasImg = pendingImages[who].length > 0;
        if (!msg && !hasImg) {
            if (sender === 'Alice') hideAliceTyping();
            else hideBobTyping();
            return;
        }

        let ratchetAction = t('symmetricStep');
        if (sender !== lastSender && lastSender !== "") {
            if (sender === 'Alice') {
                alicePriv = Math.floor(Math.random() * 10) + 2;
                alicePub  = Math.pow(G, alicePriv) % P;
                currentRootKey = computeRoot(alicePriv, bobPub);
            } else {
                bobPriv = Math.floor(Math.random() * 10) + 2;
                bobPub  = Math.pow(G, bobPriv) % P;
                currentRootKey = computeRoot(bobPriv, alicePub);
            }
            ratchetAction = t('rotateRoot');
            updateRootKeyUI();
        } else if (currentRootKey === "") {
            currentRootKey = computeRoot(alicePriv, bobPub);
            ratchetAction  = t('initHandshake');
            updateRootKeyUI();
        }

        // Send pending images as encrypted Base64 payloads
        for (const imgData of pendingImages[who]) {
            const ts = Date.now();
            const sessionKey = mode === "AES"
                ? CryptoJS.HmacSHA256(ts.toString(), currentRootKey).toString().substring(0, 16)
                : VIG_KEY;

            // 1. Hash the original image file
            const hash = await hashImage(imgData.file);
            
            // 2. Encrypt pixels
            const scrambledImageData = encryptImagePixelByPixel(imgData.imageData, sessionKey);
            
            // 3. Display scrambled in blackbox
            displayScrambledImageInBlackbox(scrambledImageData, `${tConsole('scrambledImageLabel')} (FROM ${sender.toUpperCase()})`, 
                `Hash: ${hash}<br>Session Key: ${sessionKey}<br>Size: ${imgData.width}x${imgData.height}`);

            // 4. Send encrypted pixel data as Base64
            // We'll use the ciphertext from the WordArray
            const pixels = imgData.imageData.data;
            const wordArr = CryptoJS.lib.WordArray.create(pixels);
            const encrypted = CryptoJS.AES.encrypt(wordArr, sessionKey, {
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7,
                iv: CryptoJS.enc.Hex.parse('00000000000000000000000000000000')
            });
            const encryptedBase64 = encrypted.toString();

            set(msgRef, {
                c: encryptedBase64, s: sender, ts, raw: '[IMAGE_PIXELS]', sk: sessionKey,
                m: mode, h: hash, mt: 'image',
                w: imgData.width, h_img: imgData.height,
                pub: sender === 'Alice' ? alicePub : bobPub,
                rk: currentRootKey, act: ratchetAction,
                reactions: {}
            });
        }

        if (hasImg) {
            pendingImages[who] = [];
            const strip = document.getElementById(who + 'ImgStrip');
            if (strip) { strip.innerHTML = ''; strip.classList.remove('has-images'); }
        }

        if (msg) {
            const ts = Date.now();
            const enc = encryptPayloadForMode(msg, mode, ts);
            set(msgRef, {
                c: enc.cipher, s: sender, ts, raw: msg, sk: enc.sessionKey,
                m: mode, h: enc.hash, mt: 'text',
                pub: sender === 'Alice' ? alicePub : bobPub,
                rk: currentRootKey, act: ratchetAction,
                reactions: {}
            });
        }

        lastSender = sender;
        if (sender === 'Alice') hideAliceTyping();
        else hideBobTyping();
        document.getElementById(inputId).value = "";
    };

    /* ================================================================
    REACTIONS
    ================================================================ */
    window.addReaction = function(emoji) {
        onValue(msgRef, snap => {
            const data = snap.val();
            if (!data) return;
            const reactions = data.reactions || {};
            reactions[emoji] = (reactions[emoji] || 0) + 1;
            update(msgRef, { reactions });
        }, { onlyOnce: true });
    };

    window.togglePicker = function(id) {
        const el = document.getElementById(id);
        if (el) el.style.display = el.style.display === 'flex' ? 'none' : 'flex';
    };

    /* ================================================================
    FIREBASE LISTENER
    ================================================================ */
    onValue(msgRef, snap => {
        const d = snap.val();
        if (!d) return;

        if (d.s === 'Alice') alicePub = d.pub; else bobPub = d.pub;
        currentRootKey = d.rk;
        lastSender     = d.s;
        updateRootKeyUI();

// Skip if this message was already loaded from localStorage history
        if (d.ts && _restoredTsSet.has(d.ts)) {
            _restoredTsSet.delete(d.ts); // consume — only skip once per ts
            window.lastProcessedTs = d.ts; // Ghi nhớ ID tin nhắn này
            return;
        }

        // FIX LỖI: NẾU TRÙNG ID (Chỉ thả tim) -> CẬP NHẬT GIAO DIỆN VÀ DỪNG LẠI
        if (window.lastProcessedTs === d.ts) {
            let rxHtml = '';
            const rx = d.reactions || {};
            for (const [emoji, count] of Object.entries(rx)) {
                rxHtml += `<span class="reaction-badge" onclick="addReaction('${emoji}')">${emoji} ${count}</span>`;
            }
            
            // Tìm bong bóng chat cuối cùng của Alice và Bob để cập nhật icon
            ['aliceOutput', 'bobOutput'].forEach(id => {
                const bubbles = document.querySelectorAll(`#${id} .bubble`);
                if (bubbles.length > 0) {
                    const lastBubble = bubbles[bubbles.length - 1];
                    const rxDiv = lastBubble.querySelector('.reactions');
                    if (rxDiv) rxDiv.innerHTML = rxHtml;
                }
            });

            homeHistoryUpdateReactions(d.ts, rx);

            return; // DỪNG LẠI ở đây, không tạo thêm tin nhắn mới!
        }
        
        // Lưu lại ID của tin nhắn mới nhất
        window.lastProcessedTs = d.ts;

        let decryptedMsg = "", statusText = tConsole('integrityOk'), statusColor = "#75b9e6";
        let decryptedPayload = "";
        
        if (d.mt === 'image') {
            try {
                // 1. Decrypt pixels
                const recoveredImageData = decryptImagePixelByPixel(d.c, d.w, d.h_img, d.sk);
                
                // 2. Convert to DataURL for display
                const canvas = document.createElement('canvas');
                canvas.width = d.w; canvas.height = d.h_img;
                const ctx = canvas.getContext('2d');
                ctx.putImageData(recoveredImageData, 0, 0);
                const recoveredSrc = canvas.toDataURL('image/png');
                
                // 3. Display in chat
                appendImageBubble('aliceOutput', recoveredSrc, d.s === 'Alice' ? 'self' : 'friend');
                appendImageBubble('bobOutput',   recoveredSrc, d.s === 'Bob'   ? 'self' : 'friend');
                
                decryptedMsg = '[IMAGE_PIXELS]';
                
                // 4. Display scrambled image in blackbox (received side)
                const scrambledImageData = encryptImagePixelByPixel(recoveredImageData, d.sk);
                displayScrambledImageInBlackbox(scrambledImageData, `${tConsole('receivedScrambledImageLabel')} (FOR ${d.s === 'Alice' ? 'BOB' : 'ALICE'})`, 
                    `Hash: ${d.h}<br>Session Key: ${d.sk}<br>Size: ${d.w}x${d.h_img}`);
                
                homeHistoryPush({ type:'image', src: recoveredSrc, sender: d.s === 'Alice' ? 'self-alice' : 'self-bob', ts: d.ts });
            } catch(e) {
                decryptedMsg = tConsole('imageDecryptError');
                statusText = tConsole('integrityErr'); statusColor = "#EF4444";
            }
        } else {
            try {
                const dec = decryptPayloadForMode(d);
                decryptedPayload = dec.payload || "";
                if (d.m === "AES") {
                    if (!dec.ok) { statusText = tConsole('integrityErr'); statusColor = "#EF4444"; }
                } else {
                    statusText = tConsole('statusVigenere'); statusColor = "#F59E0B";
                }
            } catch(e) {
                decryptedPayload = tConsole('decryptError');
                statusText = tConsole('integrityErr'); statusColor = "#EF4444";
            }

            const parsedImage = parseImagePayload(decryptedPayload);
            if (parsedImage) {
                appendImageBubble('aliceOutput', parsedImage.src, d.s === 'Alice' ? 'self' : 'friend');
                appendImageBubble('bobOutput',   parsedImage.src, d.s === 'Bob'   ? 'self' : 'friend');
                decryptedMsg = tConsole('decryptedImage');
                homeHistoryPush({ type:'image', src: parsedImage.src, sender: d.s === 'Alice' ? 'self-alice' : 'self-bob', ts: d.ts });
            } else {
                decryptedMsg = decryptedPayload;
                appendBubble('aliceOutput', decryptedMsg, d.s === 'Alice' ? 'self' : 'friend', d.reactions || {});
                appendBubble('bobOutput',   decryptedMsg, d.s === 'Bob'   ? 'self' : 'friend', d.reactions || {});
                homeHistoryPush({ type:'text', text:decryptedMsg, sender: d.s === 'Alice' ? 'self-alice' : 'self-bob', ts: d.ts, reactions: d.reactions || {} });
            }
        }

        /* --- Console log --- */
        const entry = buildConsoleEntry(d, decryptedMsg, statusText, statusColor);
        document.getElementById('processLog').prepend(entry);
        // Persist to localStorage so console survives refresh
        consoleLogPush({ ...d, statusText, statusColor });

        /* Save this message to home history is handled above per message type */
    });

    /* ================================================================
    HOME CHAT HISTORY — localStorage persistence
    ================================================================ */
    const HOME_HIST_KEY    = 'home_chat_log_v2';
    const HOME_CONSOLE_KEY = 'home_console_log_v2';
    // Use a Set of all restored ts values — more robust than single _lastRestoredTs
    let _restoredTsSet = new Set();
    let _lastRestoredTs = 0; // keep for backward compat

    function homeHistoryGetAll() {
        try { return JSON.parse(localStorage.getItem(HOME_HIST_KEY)) || []; }
        catch(e) { return []; }
    }

    function homeHistorySave(arr) {
        try {
            if (arr.length > 200) arr = arr.slice(arr.length - 200);
            localStorage.setItem(HOME_HIST_KEY, JSON.stringify(arr));
        } catch(e) {
            try {
                const trimmed = arr.slice(Math.floor(arr.length / 2));
                localStorage.setItem(HOME_HIST_KEY, JSON.stringify(trimmed));
            } catch(e2) {}
        }
    }

    function homeHistoryPush(item) {
        const arr = homeHistoryGetAll();
        if (item.ts && arr.some(x => x.ts === item.ts && x.type === item.type)) return;
        arr.push(item);
        homeHistorySave(arr);
    }

    function homeHistoryPushImage(src, who) {
        const arr = homeHistoryGetAll();
        arr.push({ type:'image', src, who, ts: Date.now() });
        homeHistorySave(arr);
    }

    /* ---- Console log persistence ---- */
    function consoleLogGetAll() {
        try { return JSON.parse(localStorage.getItem(HOME_CONSOLE_KEY)) || []; }
        catch(e) { return []; }
    }

    function consoleLogSave(arr) {
        try {
            if (arr.length > 50) arr = arr.slice(arr.length - 50);
            localStorage.setItem(HOME_CONSOLE_KEY, JSON.stringify(arr));
        } catch(e) {}
    }

    function consoleLogPush(entry) {
        const arr = consoleLogGetAll();
        if (entry.ts && arr.some(x => x.ts === entry.ts)) return;
        arr.push(entry);
        consoleLogSave(arr);
    }

    function buildConsoleEntry(d, decryptedMsg, statusText, statusColor) {
        const dt = new Date(d.ts);
        const timeStr = `${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}:${String(dt.getSeconds()).padStart(2,'0')} ${dt.getDate()}/${dt.getMonth()+1}`;
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <div class="log-header">
                <span class="log-badge"><i class="fas fa-${d.m==='AES'?'lock':'key'}"></i> ${d.m}</span>
                <span style="color:#75b9e6;font-size:.68rem;"><i class="far fa-clock"></i> ${timeStr}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-sync-alt"></i> ${tConsole('actionLabel')}</span>
                <span class="log-value" style="font-weight:700;background:#143a55;">${d.act}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-hashtag"></i> ${tConsole('nonceLabel')}</span>
                <span class="log-value" style="font-family:monospace;">${d.ts}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-code-branch"></i> ${tConsole('rootkeyLabel')}</span>
                <span class="key-chip" title="${tConsole('rootKeyTitle')}">${d.rk}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-key"></i> ${tConsole('sessionLabel')}</span>
                <span class="key-chip" title="${tConsole('sessionKeyTitle')}">${d.sk}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-message"></i> ${tConsole('plaintextLabel')}</span>
                <span class="log-value">${d.raw}</span>
            </div>
            <div class="log-row">
                <span class="log-label" style="font-size:.65rem;"><i class="fas fa-file-signature"></i> ${tConsole('rawDataLabel')}</span>
                <span class="log-value" style="font-family:monospace;font-size:.65rem;opacity:.75;">${d.raw}|${d.ts}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-shield-alt"></i> ${tConsole('hmacLabel')}</span>
                <span class="log-value" style="font-family:monospace;word-break:break-all;font-size:.65rem;">${d.h}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-check-circle"></i> ${tConsole('verifyLabel')}</span>
                <span class="integrity-badge" style="border-color:${statusColor};color:${statusColor};">${statusText}</span>
            </div>`;
        return entry;
    }

    function restoreConsoleLog() {
        const log = document.getElementById('processLog');
        if (!log) return;
        const entries = consoleLogGetAll();
        if (entries.length === 0) {
            // Show initial DH handshake info
            addInitHandshakeEntry();
            return;
        }
        // Restore newest-first (already stored in order, prepend reverses)
        [...entries].reverse().forEach(d => {
            let decryptedMsg = d.raw || '';
            let statusText = d.statusText || tConsole('integrityOk');
            let statusColor = d.statusColor || '#75b9e6';
            const entry = buildConsoleEntry(d, decryptedMsg, statusText, statusColor);
            log.appendChild(entry); // append in chronological order
        });
    }

    function addInitHandshakeEntry() {
        const log = document.getElementById('processLog');
        if (!log) return;
        const initRk = computeRoot(alicePriv, bobPub);
        const now = Date.now();
        const dt  = new Date(now);
        const timeStr = `${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}:${String(dt.getSeconds()).padStart(2,'0')} ${dt.getDate()}/${dt.getMonth()+1}`;
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        entry.innerHTML = `
            <div class="log-header">
                <span class="log-badge" style="background:#1a3a55;border-color:#3d8fc0;">
                    <i class="fas fa-handshake"></i> DH INIT
                </span>
                <span style="color:#75b9e6;font-size:.68rem;"><i class="far fa-clock"></i> ${timeStr}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-sync-alt"></i> ${tConsole('actionLabel')}</span>
                <span class="log-value" style="font-weight:700;background:#143a55;">${tConsole('initHandshake')}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-calculator"></i> G / P</span>
                <span class="log-value" style="font-family:monospace;">G=${G} / P=${P}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-user"></i> Alice pub</span>
                <span class="key-chip">${alicePub}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-user-astronaut"></i> Bob pub</span>
                <span class="key-chip">${bobPub}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-code-branch"></i> ${tConsole('rootkeyLabel')}</span>
                <span class="key-chip">${initRk}</span>
            </div>
            <div class="log-row">
                <span class="log-label"><i class="fas fa-check-circle"></i> ${tConsole('readyStatus')}</span>
                <span class="integrity-badge" style="border-color:#75b9e6;color:#75b9e6;">${tConsole('sessionReady')}</span>
            </div>`;
        log.prepend(entry);
    }

    function restoreHomeHistory() {
        const arr = homeHistoryGetAll();
        // Build the full set of all restored ts values (for robust duplicate prevention)
        arr.forEach(item => { if (item.ts) _restoredTsSet.add(item.ts); });
        // Also update _lastRestoredTs for backward compat
        const lastText = [...arr].reverse().find(x => x.type === 'text' && x.ts);
        if (lastText) _lastRestoredTs = lastText.ts;

        if (arr.length === 0) return;
        arr.forEach(item => {
            if (item.type === 'image') {
                const selfTypeA = item.sender
                    ? (item.sender === 'self-alice' ? 'self' : 'friend')
                    : (item.who === 'alice' ? 'self' : 'friend');
                const selfTypeB = item.sender
                    ? (item.sender === 'self-bob' ? 'self' : 'friend')
                    : (item.who === 'bob' ? 'self' : 'friend');
                appendImageBubble('aliceOutput', item.src, selfTypeA);
                appendImageBubble('bobOutput',   item.src, selfTypeB);
            } else {
                const migratedImg = parseImagePayload(item.text || '');
                if (migratedImg) {
                    const aliceType = item.sender === 'self-alice' ? 'self' : 'friend';
                    const bobType   = item.sender === 'self-bob'   ? 'self' : 'friend';
                    appendImageBubble('aliceOutput', migratedImg.src, aliceType);
                    appendImageBubble('bobOutput',   migratedImg.src, bobType);
                    return;
                }
                if (typeof item.text === 'string' && item.text.startsWith('data:image/')) {
                    const aliceType = item.sender === 'self-alice' ? 'self' : 'friend';
                    const bobType   = item.sender === 'self-bob'   ? 'self' : 'friend';
                    appendImageBubble('aliceOutput', item.text, aliceType);
                    appendImageBubble('bobOutput',   item.text, bobType);
                    return;
                }
                const aliceType = item.sender === 'self-alice' ? 'self' : 'friend';
                const bobType   = item.sender === 'self-bob'   ? 'self' : 'friend';
                appendBubble('aliceOutput', item.text, aliceType, item.reactions || {});
                appendBubble('bobOutput',   item.text, bobType, item.reactions ||  {});
            }
        });
    }

    window.clearHomeChat = function() {
        if (!confirm(t('deleteAllChatConfirm'))) return;
        localStorage.removeItem(HOME_HIST_KEY);
        localStorage.removeItem(HOME_CONSOLE_KEY);
        localStorage.setItem('stat_msg', '0');
        localStorage.setItem('stat_img', '0');
        localStorage.setItem('stat_enc', '0');
        _lastRestoredTs = 0;
        _restoredTsSet  = new Set();

        const aliceOut = document.getElementById('aliceOutput');
        const bobOut   = document.getElementById('bobOutput');
        const specials = {
            aliceSeen:    document.getElementById('aliceSeenIndicator'),
            bobTypingB:   document.getElementById('bobTypingBubble'),
            bobTypingL:   document.getElementById('bobTypingLabel'),
            aliceTypingB: document.getElementById('aliceTypingBubble'),
            aliceTypingL: document.getElementById('aliceTypingLabel'),
            bobSeen:      document.getElementById('bobSeenIndicator')
        };
        if (aliceOut) {
            aliceOut.innerHTML = '';
            if (specials.aliceSeen)  aliceOut.appendChild(specials.aliceSeen);
            if (specials.bobTypingB) aliceOut.appendChild(specials.bobTypingB);
            if (specials.bobTypingL) aliceOut.appendChild(specials.bobTypingL);
        }
        if (bobOut) {
            bobOut.innerHTML = '';
            if (specials.aliceTypingB) bobOut.appendChild(specials.aliceTypingB);
            if (specials.aliceTypingL) bobOut.appendChild(specials.aliceTypingL);
            if (specials.bobSeen)      bobOut.appendChild(specials.bobSeen);
        }
        // Reset console to initial state
        const log = document.getElementById('processLog');
        if (log) { log.innerHTML = ''; addInitHandshakeEntry(); }
        showToast(t('deleteAllChatSuccess'));
        updateAccountStats();
    };

    /* ================================================================
    APPEND BUBBLE
    ================================================================ */
    function appendBubble(containerId, text, type, reactions) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const div  = document.createElement('div');
        div.className = `bubble ${type}`;
        const time = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });

        let reactionsHtml = '';
        for (const [emoji, count] of Object.entries(reactions))
            reactionsHtml += `<span class="reaction-badge" onclick="addReaction('${emoji}')">${emoji} ${count}</span>`;

        const pid = 'picker-' + Math.random().toString(36).substr(2, 8);

        div.innerHTML = `${text}
            <span class="timestamp"><i class="far fa-clock"></i> ${time}</span>
            <div class="reactions">${reactionsHtml}</div>
            <div class="quick-reactions">
                <span class="quick-reaction-icon" onclick="addReaction('👍')">👍</span>
                <span class="quick-reaction-icon" onclick="addReaction('❤️')">❤️</span>
                <span class="quick-reaction-icon" onclick="addReaction('😂')">😂</span>
                <span class="quick-reaction-icon" onclick="addReaction('😮')">😮</span>
                <span class="quick-reaction-icon" onclick="addReaction('😢')">😢</span>
                <div id="${pid}" class="reaction-picker" style="display:none;" onclick="event.stopPropagation()">
                    <span onclick="addReaction('👍');togglePicker('${pid}')">👍</span>
                    <span onclick="addReaction('❤️');togglePicker('${pid}')">❤️</span>
                    <span onclick="addReaction('😂');togglePicker('${pid}')">😂</span>
                    <span onclick="addReaction('😮');togglePicker('${pid}')">😮</span>
                    <span onclick="addReaction('😢');togglePicker('${pid}')">😢</span>
                    <span onclick="addReaction('😡');togglePicker('${pid}')">😡</span>
                </div>
            </div>`;

        // Insert before typing-bubble / seen-indicator if present
        const typingBubble = container.querySelector('.typing-bubble');
        const typingLabel  = container.querySelector('.typing-label');
        const seenInd      = container.querySelector('.seen-indicator');

        if (typingBubble) container.insertBefore(div, typingBubble);
        else if (seenInd) container.insertBefore(div, seenInd);
        else container.appendChild(div);

        container.scrollTop = container.scrollHeight;
    }

    /* ================================================================
    I18N — TRANSLATION SYSTEM
    ================================================================ */
    let currentLang = 'vi'; // 'vi' | 'en'
    let consoleLang = 'vi'; // Blackbox always stays in Vietnamese

    const i18nStrings = {
        vi: {
            // Nav
            navProject: 'Dự án',
            navHome: 'Trang chủ', navFriends: 'Bạn bè', navAccount: 'Tài khoản', navTeam: 'Đội ngũ',
            // Utility Hub
            hubLanguage: 'Ngôn ngữ',
            hubTheme: 'Giao diện',
            hubConsole: 'Console',
            // Buttons
            send: 'Gửi', hideConsole: 'Ẩn Console', showConsole: 'Hiện Console',
            // Status
            online: 'Đang hoạt động',
            aliceName: 'Alice (Bạn)',
            // Seen / typing
            seenBy: 'Bob đã xem',
            aliceSeenBy: 'Alice đã xem',
            typing: 'Alice đang nhập...',
            bobTyping: 'Bob đang nhập...',
            // Console header
            ratchetTitle: 'RATCHET MONITOR',
            // Log labels
            actionLabel: 'Hành động', nonceLabel: 'Số ngẫu nhiên', rootkeyLabel: 'Khóa gốc',
            sessionLabel: 'Khóa phiên', plaintextLabel: 'Bản rõ',
            hashLabel: 'Hash', verifyLabel: 'Kiểm tra', rawDataLabel: 'Dữ liệu thô', hmacLabel: 'HMAC-SHA256',
            // Integrity
            integrityOk: '✅ TOÀN VẸN', integrityErr: '❌ LỖI',
            // Ratchet actions
            symmetricStep: 'SYMMETRIC STEP (TIẾP TỤC PHIÊN)',
            rotateRoot: 'XOAY ROOT KEY (DH Ratchet)',
            initHandshake: 'KHỞI TẠO HANDSHAKE',
            // Theme / lang toggle labels
            switchToDark: 'Tối', switchToLight: 'Sáng',
            switchToEN: 'EN', switchToVI: 'VI',
            teamTitle: 'Dự án: Secure Messenger & The Hacker View',
            teamDesc: 'Mô phỏng ứng dụng nhắn tin bảo mật và thực nghiệm các kịch bản tấn công thực tế để làm rõ ranh giới giữa mã hóa mạnh và rủi ro từ yếu tố con người.',
            roleLeader: 'NHÓM TRƯỞNG',
            roleDev: 'THÀNH VIÊN',
            roleSec: 'THÀNH VIÊN',
            roleQA: 'THÀNH VIÊN',
            roleData: 'THÀNH VIÊN',
            taskLeader: 'Đề xuất ý tưởng và xây dựng luồng xử lý chính; Phát triển giao diện demo; Tối ưu thuật toán mã hóa.',
            taskDev1: 'Tinh chỉnh giao diện người dùng (UI/UX); Nghiên cứu và tích hợp tính năng; Quản lý nội dung hiển thị.',
            taskDev2: 'Xây dựng bản demo kỹ thuật (PoC) bằng Java; Lập trình tính năng mở rộng; Phát triển Web Modules.',
            taskSec: 'Mô hình hóa mã hóa AES, trao đổi khóa Diffie–Hellman và luồng HMAC trong demo.',
            taskQA: 'Thực hiện kiểm thử xâm nhập (Pen-test); Mô phỏng các kịch bản tấn công để kiểm tra hệ thống.',
            taskData: 'Phân tích luồng dữ liệu, tài liệu kỹ thuật và hỗ trợ trình bày.',
            taskParticipated: 'Có tham gia',
            teamPageKicker: 'Thành viên nhóm',
            teamPageTitle: 'ĐỘI NGŨ DỰ ÁN',
            teamIntro: 'Chúng mình là nhóm sinh viên thực hiện dự án Secure Messenger, cùng chung đam mê về bảo mật thông tin và nỗ lực hiện thực hóa ý tưởng xây dựng một ứng dụng nhắn tin an toàn đầu cuối.',
            statusVigenere: '⚠️ Vigenère (demo)',
            navAccount: 'Tài khoản',
            changeAvatar: 'Đổi ảnh đại diện',
            newDisplayName: 'Tên hiển thị mới',
            newEmail: 'Email mới',
            saveChanges: 'LƯU THAY ĐỔI',
            cancelBtn: 'HỦY',
            displayNameLabel: 'Tên hiển thị:',
            emailLabel: 'Email:',
            newNamePlaceholder: 'Nhập tên mới...',
            newEmailPlaceholder: 'Nhập email mới...',
            updateNameSuccess: '✅ Đã cập nhật Tên hiển thị thành công!',
            deleteAllChat: 'Xóa toàn bộ đoạn chat',
            deleteAllChatConfirm: 'Xóa toàn bộ lịch sử đoạn chat Alice ↔ Bob?',
            deleteAllChatSuccess: '🗑️ Đã xóa toàn bộ đoạn chat!',
            deleteAllMessagesConfirm: 'Xóa toàn bộ tin nhắn với',
            noMessages: 'Chưa có tin nhắn',
            justNow: 'Vừa xong',
            greetingDefault: 'Chào bạn, mình là',
            greetingResponse1: 'Chào',
            friendGreeting: 'Chào bạn!',
            friendReplies: ['Cảm ơn tin nhắn của bạn!', 'Mình hiểu rồi 👍', 'Ok bạn nhé!', 'Hay đấy 😊', 'Mình sẽ kiểm tra lại!'],
            sendImage: 'Gửi ảnh',
            messageSent: '💬 Đã gửi tin nhắn!',
            invalidEmail: 'Vui lòng nhập đúng định dạng email',
            authModalTitle: 'Alice (Bạn)',
            loginSuccess: 'Đăng nhập thành công: ',
            loginToView: 'Vui lòng đăng nhập để xem trang này',
            loginTourTitle: 'ĐĂNG NHẬP HỆ THỐNG',
            loginTourDesc: 'Để trải nghiệm đầy đủ tính năng mã hóa E2E, bạn cần đăng nhập tài khoản Alice. Hãy nhấn vào đây để bắt đầu.',
            loginTourSuccess: 'Đăng nhập thành công! Tiếp tục tour...',
            loginTourPrompt: 'Vui lòng nhập thông tin đăng nhập!',
            alreadyLoggedIn: 'Bạn đã đăng nhập rồi!',
            continueWithoutLogin: 'Bạn có muốn tiếp tục tour mà không đăng nhập?',
            loginFormNameTitle: 'NHẬP TÊN TÀI KHOẢN',
            loginFormNameDesc: 'Nhập "Alice" vào ô tên tài khoản',
            loginFormEmailTitle: 'NHẬP EMAIL',
            loginFormEmailDesc: 'Nhập "alice@example.com" vào ô email',
            deleteFriendMessagesTitle: 'Xóa tin nhắn với ',
            typerIsTyping: ' đang nhập tin nhắn...',
            logoutConfirm: 'Đăng xuất tài khoản?',
            logoutSuccess: '👋 Đã đăng xuất',
            accountSaveSuccess: '✅ Đã lưu thông tin tài khoản!',
            avatarUpdateSuccess: '🖼️ Đã cập nhật avatar Alice',
            // === LOGIN PAGE ===
            loginPortalTitle: 'Portal Đăng Nhập Secure Messenger',
            loginPortalDesc: 'Đăng nhập để truy cập toàn bộ mô phỏng bảo mật: Diffie-Hellman handshake, AES-256 encryption, SHA-256 integrity và các kịch bản tấn công thực tế theo góc nhìn Hacker View.',
            realtimeSecure: 'Ứng Dụng Secure Messenger Realtime',
            badgeAES: 'AES-256 + SHA-256',
            badgeThreat: 'Mô Phỏng Tấn Công',
            bootMessage: '[KHỞI ĐỘ] Khởi tạo thời gian chạy bảo mật...',
            cryptoDHMessage: '[MÃ HÓA] Sẵn sàng trao đổi khóa DH',
            cryptoAESMessage: '[MÃ HÓA] Khóa phiên AES-256 được khóa',
            verifyIntegrityMessage: '[XÁC MINH] Giám sát toàn vẹn SHA-256 hoạt động',
            authTitle: 'Đăng nhập Alice',
            authNameLabel: 'Tên',
            authNamePlaceholder: 'Nhập tên tài khoản',
            authEmailLabel: 'Email',
            authEmailPlaceholder: 'alice@example.com',
            authClose: 'Đóng',
            authLogin: 'Đăng nhập',
            // === KỊCH BẢN ATTACKER (EVE) ===
            xssTitle: 'Xác thực bảo mật',
            xssDesc: 'Đồng bộ khóa AES thất bại. Vui lòng nhập mật khẩu hiện tại để khôi phục phiên làm việc và tiếp tục giải mã tin nhắn.',
            currPwd: 'Mật khẩu hiện tại',
            verifyBtn: 'Xác nhận',
            xssCancel: 'Hủy',
            hackedName: '⚠️ Attacker (Eve) — chiếm quyền hiển thị',
            compromised: 'Bị khống chế',
            accLocked: 'TÀI KHOẢN ĐÃ BỊ KHÓA...',
            sysBreached: 'HỆ THỐNG BỊ XÂM NHẬP',
            hackerInject: 'Attacker (Eve): Đang mô phỏng tiêm XSS (Cross-Site Scripting)...',
            hackerAlertTitle: 'CẢNH BÁO HỆ THỐNG',
            hackerAlertBody: 'Cảnh báo giả lập từ Attacker (Eve). Thông báo lỗi đồng bộ khóa AES.<br><br>Nhấn',
            hackerAlertLink: 'để “xác thực” (mô phỏng social engineering).',
            takeoverSuccess: '🚨 Mô phỏng chiếm quyền thành công — Attacker (Eve) đã kiểm soát giao diện Alice.',
            pwdRequired: '⚠️ Vui lòng nhập mật khẩu hiện tại để tiếp tục!',
            hackBtn: 'KẺ TẤN CÔNG',
            readyStatus: 'Sẵn sàng',
            sessionReady: '✅ PHIÊN SẴN SÀNG',
            decryptError: '[Lỗi giải mã]',
            imageDecryptError: '[Lỗi giải mã ảnh pixel]',
            decryptedImage: '[Ảnh đã giải mã]',
            rootKeyTitle: 'Khóa gốc từ Diffie-Hellman',
            sessionKeyTitle: 'Khóa phiên dùng cho mã hóa',
            vigenereKeyTitle: 'Từ khóa dùng cho Vigenère',
            scrambledImageLabel: 'ẢNH ĐÃ MÃ HÓA',
            receivedScrambledImageLabel: 'NHẬN ẢNH ĐÃ MÃ HÓA',
            hackerBreach: "[HỆ THỐNG] PHÁT HIỆN XÂM NHẬP...",
            hackerSource: "[THÔNG TIN] NGUỒN: CLICK VÀO LINK PHISHING",
            hackerWarn: "[CẢNH BÁO] LỖ HỔNG MẬT KHẨU BỊ KHAI THÁC",
            hackerAccess: "[HACK] ĐANG TRUY CẬP KHÓA GỐC...",
            hackerRotate: "[HACK] KHÓA GỐC BỊ XOAY BỞI KẺ TẤN CÔNG",
            hackerExfil: "[XÂM NHẬP] ĐANG TRÍCH XUẤT DỮ LIỆU...",
            hackerCompromised: "[LỖI] LỚP BẢO MẬT BỊ THAO TÚNG",
            hackerTakeover: "!!! TÀI KHOẢN ĐÃ BỊ CHIẾM QUYỀN !!!",
            threatSimLoaded: "[BẢO MẬT] Đã tải module mô phỏng mối đe dọa",
            xssDesc: 'Phiên đăng nhập đã hết hạn. Vui lòng nhập lại mật khẩu để tiếp tục đồng bộ tin nhắn mã hóa.',
            langTitle: 'Ngôn ngữ',
            themeTitle: 'Giao diện',
            helpTitle: 'Hướng dẫn',
            authLabelLogin: 'Đăng nhập',
            authLabelLogout: 'Đăng xuất',
            aliceNameWithYou: 'Alice (Bạn)',
            friendsTitle: 'Bạn bè',
            searchFriendsPlaceholder: 'Tìm kiếm bạn bè...',
            sendLabel: 'Gửi',
            dropAvatarTitle: 'Kéo thả ảnh vào đây để đổi avatar',
            onlineStatus: 'Đang trực tuyến',
            changePhoto: 'Đổi ảnh',
            statSent: 'Tin đã gửi',
            statFriends: 'Bạn bè',
            statImages: 'Ảnh đã gửi',
            statCrypto: 'Mã hoá',
            personalInfo: 'Thông tin cá nhân',
            labelName: 'Tên',
            labelStatus: 'Trạng thái',
            statusActive: 'Đang hoạt động',
            saveChanges: 'Lưu thay đổi',
            badgesTitle: 'Huy hiệu',
            badgeExpert: 'Bảo mật Expert',
            badgeExpertDesc: 'Dùng AES encryption',
            badgeChatter: 'Người trò chuyện',
            badgeChatterDesc: 'Gửi tin nhắn đầu tiên',
            badgeConnector: 'Kết nối cộng đồng',
            badgeConnectorDesc: '8 bạn bè trong danh sách',
            badgeSpeed: 'Siêu tốc độ',
            badgeSpeedDesc: 'Gửi 50 tin nhắn',
            weeklyActivity: 'Hoạt động tuần',
            mon: 'T2', tue: 'T3', wed: 'T4', thu: 'T5', fri: 'T6', sat: 'T7', sun: 'CN',
        },
        en: {
            navProject: 'Project',
            navHome: 'Home', navFriends: 'Friends', navAccount: 'Account', navTeam: 'Team',
            // Utility Hub
            hubLanguage: 'Language',
            hubTheme: 'Theme',
            hubConsole: 'Console',
            send: 'Send', hideConsole: 'Hide Console', showConsole: 'Show Console',
            online: 'Online',
            aliceName: 'Alice (You)',
            seenBy: 'Seen by Bob',
            aliceSeenBy: 'Seen by Alice',
            typing: 'Alice is typing...',
            bobTyping: 'Bob is typing...',
            ratchetTitle: 'RATCHET MONITOR',
            actionLabel: 'Action', nonceLabel: 'Nonce', rootkeyLabel: 'Root Key',
            sessionLabel: 'Session Key', plaintextLabel: 'Plaintext',
            hashLabel: 'Hash', verifyLabel: 'Verify', rawDataLabel: 'Raw Data', hmacLabel: 'HMAC-SHA256',
            integrityOk: '✅ INTACT', integrityErr: '❌ ERROR',
            symmetricStep: 'SYMMETRIC STEP (CONTINUE SESSION)',
            rotateRoot: 'ROTATE ROOT KEY (DH Ratchet)',
            initHandshake: 'INIT HANDSHAKE',
            switchToDark: 'Dark', switchToLight: 'Light',
            switchToEN: 'EN', switchToVI: 'VI',
            teamTitle: 'Project: Secure Messenger & The Hacker View',
            teamDesc: 'A simulation of secure messaging and realistic attack scenarios, showing how strong cryptography can still fail due to human factors.',
            roleLeader: 'TEAM LEADER',
            roleDev: 'TEAM MEMBER',
            roleSec: 'TEAM MEMBER',
            roleQA: 'TEAM MEMBER',
            roleData: 'TEAM MEMBER',
            taskLeader: 'Project ideation and core logic flow; UI demo development; Encryption algorithm optimization.',
            taskDev1: 'UI/UX refinement; Feature research and integration; Content and data management.',
            taskDev2: 'Technical PoC development (Java); Extended features programming; Web modules implementation.',
            taskSec: 'Cryptography modeling: AES, Diffie–Hellman, and HMAC flows in the demo.',
            taskQA: 'Penetration testing; Vulnerability simulation to evaluate system security.',
            taskData: 'Data-flow analysis, technical writing, and presentation support.',
            taskParticipated: 'Participated',
            teamPageKicker: 'Team roster',
            teamPageTitle: 'PROJECT TEAM',
            teamIntro: 'We are the student team behind Secure Messenger, passionate about information security and working together to build a secure end-to-end messaging application.',
            statusVigenere: '⚠️ Vigenère (demo)',
            navAccount: 'Account',
            changeAvatar: 'Change Avatar',
            newDisplayName: 'New Display Name',
            newEmail: 'New Email',
            saveChanges: 'SAVE CHANGES',
            cancelBtn: 'CANCEL',
            displayNameLabel: 'Display Name:',
            emailLabel: 'Email:',
            newNamePlaceholder: 'Enter new name...',
            newEmailPlaceholder: 'Enter new email...',
            updateNameSuccess: '✅ Display name updated successfully!',
            deleteAllChat: 'Delete all chat',
            deleteAllChatConfirm: 'Delete all chat history between Alice ↔ Bob?',
            deleteAllChatSuccess: '🗑️ All chat deleted!',
            deleteAllMessagesConfirm: 'Delete all messages with',
            noMessages: 'No messages',
            justNow: 'Just now',
            greetingDefault: 'Hello, I am',
            greetingResponse1: 'Hello',
            friendGreeting: 'Hello!',
            friendReplies: ['Thanks for your message!', 'Got it 👍', 'Ok buddy!', 'That\'s great 😊', 'I will check again!'],
            sendImage: 'Send image',
            messageSent: '💬 Message sent!',
            invalidEmail: 'Please enter a valid email format',
            loginSuccess: 'Login successful: ',
            loginToView: 'Please log in to view this page',
            loginTourTitle: 'SYSTEM LOGIN',
            loginTourDesc: 'To experience full E2E encryption features, you need to login to Alice account. Click here to start.',
            loginTourSuccess: 'Login successful! Continuing tour...',
            loginTourPrompt: 'Please enter login information!',
            alreadyLoggedIn: 'You are already logged in!',
            continueWithoutLogin: 'Do you want to continue tour without login?',
            loginFormNameTitle: 'ENTER ACCOUNT NAME',
            loginFormNameDesc: 'Enter "Alice" in the account name field',
            loginFormEmailTitle: 'ENTER EMAIL',
            loginFormEmailDesc: 'Enter "alice@example.com" in the email field',
            deleteFriendMessagesTitle: 'Delete messages with ',
            typerIsTyping: ' is typing a message...',
            logoutConfirm: 'Logout account?',
            logoutSuccess: '👋 Logged out',
            accountSaveSuccess: '✅ Account information saved!',
            avatarUpdateSuccess: '🖼️ Updated Alice avatar',
            // === LOGIN PAGE ===
            loginPortalTitle: 'Secure Messenger Login Portal',
            loginPortalDesc: 'Log in to access the full security simulation: Diffie-Hellman handshake, AES-256 encryption, SHA-256 integrity and realistic attack scenarios from the Hacker\'s perspective.',
            realtimeSecure: 'Realtime Secure Messenger',
            badgeAES: 'AES-256 + SHA-256',
            badgeThreat: 'Threat Simulation',
            bootMessage: '[BOOT] Initializing secure runtime...',
            cryptoDHMessage: '[CRYPTO] DH key exchange ready',
            cryptoAESMessage: '[CRYPTO] AES-256 session lock enabled',
            verifyIntegrityMessage: '[VERIFY] SHA-256 integrity monitor online',
            threatSimLoaded: '[SECURITY] Threat simulation module loaded',
            authTitle: 'Login Alice',
            authNameLabel: 'Name',
            authNamePlaceholder: 'Enter account name',
            authEmailLabel: 'Email',
            authEmailPlaceholder: 'alice@example.com',
            authClose: 'Close',
            authLogin: 'Login',
            // === ATTACKER (EVE) SCENARIO ===
            xssTitle: 'Security Verification',
            xssDesc: 'AES key synchronization failed. Please enter your current password to restore the session and continue decrypting messages.',
            currPwd: 'Current Password',
            verifyBtn: 'Verify',
            xssCancel: 'Cancel',
            hackedName: '⚠️ Attacker (Eve) — UI takeover',
            compromised: 'Compromised',
            accLocked: 'ACCOUNT LOCKED...',
            sysBreached: 'SYSTEM BREACHED',
            hackerInject: 'Attacker (Eve): Simulated XSS (Cross-Site Scripting) injection...',
            hackerAlertTitle: 'SYSTEM ALERT',
            hackerAlertBody: 'Simulated alert from Attacker (Eve). Fake AES key sync failure.<br><br>Click',
            hackerAlertLink: 'to “verify” (social engineering simulation).',
            takeoverSuccess: '🚨 Simulated takeover complete — Attacker (Eve) controls Alice’s UI.',
            pwdRequired: '⚠️ Please enter your current password to proceed!',
            hackBtn: 'HACKER CONSOLE',
            readyStatus: 'Ready',
            sessionReady: '✅ SESSION READY',
            decryptError: '[Decryption Error]',
            imageDecryptError: '[Pixel Decryption Error]',
            decryptedImage: '[Decrypted Image]',
            rootKeyTitle: 'Root key from Diffie-Hellman',
            sessionKeyTitle: 'Session key for encryption',
            vigenereKeyTitle: 'Keyword used for Vigenère',
            scrambledImageLabel: 'ENCRYPTED IMAGE',
            receivedScrambledImageLabel: 'RECEIVED ENCRYPTED IMAGE',
            hackerBreach: "[SYSTEM] BREACH DETECTED...",
            hackerSource: "[INFO] SOURCE: PHISHING LINK CLICKED",
            hackerWarn: "[WARN] PASSWORD VULNERABILITY EXPLOITED",
            hackerAccess: "[HACK] ACCESSING ROOT_KEY...",
            hackerRotate: "[HACK] ROOT_KEY ROTATED BY ADVERSARY",
            hackerExfil: "[BREACH] DATA EXFILTRATION IN PROGRESS...",
            hackerCompromised: "[ERROR] SECURITY LAYER COMPROMISED",
            hackerTakeover: "!!! ACCOUNT HAS BEEN TAKEN OVER !!!",
            threatSimLoaded: '[SECURITY] Threat simulation module loaded',
            xssDesc: 'Session expired. Please re-enter your password to continue syncing encrypted messages.',
            langTitle: 'Language',
            themeTitle: 'Appearance',
            helpTitle: 'Help',
            authLabelLogin: 'Login',
            authLabelLogout: 'Logout',
            aliceNameWithYou: 'Alice (You)',
            friendsTitle: 'Friends',
            searchFriendsPlaceholder: 'Search friends...',
            sendLabel: 'Send',
            dropAvatarTitle: 'Drag & drop image here to change avatar',
            onlineStatus: 'Online',
            changePhoto: 'Change Photo',
            statSent: 'Sent',
            statFriends: 'Friends',
            statImages: 'Images',
            statCrypto: 'Crypto',
            personalInfo: 'Personal Info',
            labelName: 'Name',
            labelStatus: 'Status',
            statusActive: 'Active',
            saveChanges: 'Save Changes',
            badgesTitle: 'Badges',
            badgeExpert: 'Security Expert',
            badgeExpertDesc: 'Use AES encryption',
            badgeChatter: 'Chatter',
            badgeChatterDesc: 'Send first message',
            badgeConnector: 'Connector',
            badgeConnectorDesc: '8 friends in list',
            badgeSpeed: 'High Speed',
            badgeSpeedDesc: 'Send 50 messages',
            weeklyActivity: 'Weekly Activity',
            mon: 'Mon', tue: 'Tue', wed: 'Wed', thu: 'Thu', fri: 'Fri', sat: 'Sat', sun: 'Sun',
        }
    };

    function t(key, lang = null) {
        const useLang = lang || currentLang;
        return (i18nStrings[useLang] || i18nStrings['vi'])[key] || key;
    }

    // Translate for console/blackbox
    function tConsole(key) {
        return t(key);
    }

    const TEAM_PROFILE_BODIES = {
        vi: {
            1: '<p><strong>Vai trò:</strong> Trưởng nhóm / kiến trúc sư hệ thống.</p><ul><li>Hoạch định phạm vi, rủi ro và timeline trình diễn.</li><li>Đối chiếu yêu cầu môn học với phần demo mật mã.</li><li>Chuẩn bị tài liệu và phân chia trách nhiệm nhóm.</li></ul>',
            2: '<p><strong>Vai trò:</strong> Thiết kế &amp; frontend.</p><ul><li>Thiết kế luồng màn hình Home, Friends, Account và trang Dự án/Đội ngũ.</li><li>Đảm bảo hiển thị nhất quán sáng/tối và i18n.</li><li>Tối ưu khả năng trình chiếu (demo/presentation).</li></ul>',
            3: '<p><strong>Vai trò:</strong> Tích hợp backend-as-a-service.</p><ul><li>Cấu hình Firebase Realtime Database cho luồng tin nhắn mẫu.</li><li>Đồng bộ trạng thái và xử lý lỗi mạng cơ bản.</li><li>Phối hợp với frontend về cấu trúc dữ liệu.</li></ul>',
            4: '<p><strong>Vai trò:</strong> Mật mã &amp; mô phỏng.</p><ul><li>Triển khai AES + HMAC-SHA256 và chế độ Vigenère minh họa.</li><li>Diễn giải Diffie–Hellman, nonce/timestamp trong console.</li><li>Đảm bảo thuật ngữ chính xác (HMAC không gọi nhầm là biến thể AES).</li></ul>',
            5: '<p><strong>Vai trò:</strong> QA / kiểm thử.</p><ul><li>Kịch bản gửi tin, ảnh, đổi chế độ mã hóa.</li><li>Kiểm thử kịch bản Attacker (Eve) và khôi phục trạng thái.</li><li>Ghi nhận lỗi giao diện và hồi quy trước khi nộp.</li></ul>',
            6: '<p><strong>Vai trò:</strong> Dữ liệu &amp; tài liệu.</p><ul><li>Sơ đồ luồng dữ liệu Alice–Bob–Firebase.</li><li>Biên tập mô tả dự án, checklist trình bày.</li><li>Hỗ trợ slide/giải thích khái niệm cho giảng viên.</li></ul>'
        },
        en: {
            1: '<p><strong>Role:</strong> Team lead / system architect.</p><ul><li>Scope, risk, and demo timeline planning.</li><li>Align course requirements with the cryptography demo.</li><li>Documentation and work split across the team.</li></ul>',
            2: '<p><strong>Role:</strong> Design &amp; frontend.</p><ul><li>UX for Home, Friends, Account, and Project/Team pages.</li><li>Consistent light/dark themes and i18n.</li><li>Presentation-friendly layouts.</li></ul>',
            3: '<p><strong>Role:</strong> BaaS integration.</p><ul><li>Firebase Realtime Database wiring for sample traffic.</li><li>Basic sync/error handling.</li><li>Data shapes coordinated with the UI.</li></ul>',
            4: '<p><strong>Role:</strong> Cryptography &amp; simulation.</p><ul><li>AES + HMAC-SHA256 and didactic Vigenère mode.</li><li>Explain DH, nonce/timestamp in the console.</li><li>Correct terminology (HMAC is not an “AES variant”).</li></ul>',
            5: '<p><strong>Role:</strong> QA / testing.</p><ul><li>Scenarios for text, images, and cipher modes.</li><li>Attacker (Eve) flows and state recovery checks.</li><li>UI regression before submission.</li></ul>',
            6: '<p><strong>Role:</strong> Data &amp; documentation.</p><ul><li>Alice–Bob–Firebase data-flow diagrams.</li><li>Project copy and presentation checklists.</li><li>Support explanations for instructors.</li></ul>'
        }
    };

    function applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = t(key);
        });
        // Update placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = t(key);
        });
        // Update titles
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = t(key);
        });
        // Update friend delete button titles
        document.querySelectorAll('.friend-delete-btn[data-friend-name]').forEach(el => {
            const friendName = el.getAttribute('data-friend-name');
            el.title = t('deleteFriendMessagesTitle') + friendName;
        });
        updateContent();
        // Update toggle button labels
        const langLabel = document.getElementById('langLabel');
        if (langLabel) langLabel.textContent = currentLang === 'vi' ? t('switchToEN') : t('switchToVI');
        const themeLabel = document.getElementById('themeLabel');
        const darkNow = document.body.classList.contains('dark-mode');
        if (themeLabel) themeLabel.textContent = darkNow ? t('switchToLight') : t('switchToDark');
        updateAuthUI();

        // Re-render console log to apply new language
        const log = document.getElementById('processLog');
        if (log) {
            log.innerHTML = '';
            restoreConsoleLog();
        }
    }

    const projectData = {
        vi: {
            kicker: { icon: 'fa-microchip', text: 'Dự án' },
            title: {
                icon: 'fa-shield-heart',
                text: 'HỆ THỐNG MÔ PHỎNG GIAO THỨC MẬT MÃ ĐA LỚP VÀ PHÂN TÍCH LỖ HỔNG TẦNG ỨNG DỤNG'
            },
            intro: [
                'Dự án được xây dựng nhằm mục đích thực nghiệm và mô phỏng các tiêu chuẩn <strong>mật mã học hiện đại</strong> trong môi trường truyền tin <strong>an toàn đầu cuối (End-to-End Encryption)</strong>. Hệ thống tập trung vào việc hiện thực hóa quy trình <strong>thiết lập khóa an toàn</strong>, <strong>mã hóa dữ liệu khối</strong> và <strong>kiểm tra tính toàn vẹn</strong>. Đồng thời, dự án cung cấp công cụ phân tích sự khác biệt giữa mật mã cổ điển và hiện đại, cũng như các rủi ro bảo mật phát sinh từ các cuộc tấn công <strong>chiếm quyền điều khiển phiên (Session Hijacking)</strong>.'
            ],
            sections: {
                architectureTitle: 'KIẾN TRÚC BẢO MẬT VÀ CƠ CHẾ VẬN HÀNH',
                accordion: [
                    {
                        icon: 'fa-exchange-alt',
                        title: 'Diffie-Hellman (Trao đổi khóa)',
                        body: [
                            'Hệ thống sử dụng giao thức <strong>Diffie-Hellman</strong> để thiết lập một <strong>khóa bí mật chung (Shared Secret)</strong> giữa hai bên (Alice và Bob) mà không cần truyền trực tiếp khóa qua kênh truyền không an toàn.',
                            'Tham số khởi tạo sử dụng cặp <strong>(P, G) = (23, 5)</strong>. Mỗi bên tạo khóa riêng tư và tính khóa công khai tương ứng. Sau khi trao đổi khóa công khai, hai bên suy ra cùng một giá trị bí mật chung làm tiền đề tạo khóa phiên.'
                        ],
                        tech: ['P = 23', 'G = 5'],
                        diagram: { type: 'dh' }
                    },
                    {
                        icon: 'fa-lock',
                        title: 'AES-256-CBC (Mã hóa khối hiện đại)',
                        body: [
                            '<strong>AES-256</strong> là tiêu chuẩn mã hóa đối xứng khối được sử dụng để bảo vệ nội dung tin nhắn.',
                            'Chế độ <strong>CBC (Cipher Block Chaining)</strong> liên kết các khối dữ liệu thông qua phép XOR với khối trước đó và sử dụng <strong>IV ngẫu nhiên</strong> để đảm bảo tính duy nhất của bản mã, kể cả khi bản rõ giống nhau.'
                        ],
                        tech: ['256-bit', 'CBC', 'IV'],
                        diagram: { type: 'aes' }
                    },
                    {
                        icon: 'fa-key',
                        title: 'Vigenère (Mật mã cổ điển)',
                        body: [
                            '<strong>Vigenère</strong> được triển khai như một đối tượng so sánh nhằm minh họa sự tiến hóa của mật mã học.',
                            'Thuật toán dựa trên <strong>từ khóa</strong> để dịch chuyển ký tự theo thay thế đa bảng chữ, nhưng dễ bị bẻ gãy bởi <strong>phân tích tần suất</strong> và không phù hợp cho môi trường kỹ thuật số hiện đại.'
                        ],
                        tech: ['Keyword', 'Polyalphabetic'],
                        diagram: { type: 'vig', keyword: 'VIGENERE' }
                    },
                    {
                        icon: 'fa-shield-alt',
                        title: 'HMAC-SHA256 (Xác thực và toàn vẹn)',
                        body: [
                            'Hệ thống sử dụng <strong>HMAC</strong> để phát hiện mọi thay đổi trên đường truyền bằng cách tạo <strong>chữ ký</strong> từ bản mã và khóa phiên.',
                            'Nếu Eve can thiệp chỉnh sửa bản mã, chữ ký tại phía nhận sẽ không trùng khớp và hệ thống kích hoạt cảnh báo <strong>mất an toàn thông tin</strong>.'
                        ],
                        tech: ['HMAC', 'SHA-256'],
                        diagram: { type: 'hmac' }
                    }
                ],
                dataJourney: {
                    title: 'Sơ đồ luồng dữ liệu động (Data Journey)',
                    subtitle: 'Alice (Người gửi) ➔ [Hầm mã hóa] ➔ Đám mây dữ liệu ➔ Bob (Người nhận)',
                    nodes: [
                        { className: 'dj-alice', icon: 'fa-paper-plane', label: 'Alice', sub: 'Người gửi' },
                        { className: 'dj-vault', icon: 'fa-vault', label: 'Hầm mã hóa', sub: 'Mã hóa + HMAC' },
                        { className: 'dj-firebase', icon: 'fa-cloud', label: 'Đám mây dữ liệu', sub: 'Kênh truyền', showEve: true },
                        { className: 'dj-bob', icon: 'fa-inbox', label: 'Bob', sub: 'Người nhận • Giải mã' }
                    ]
                },
                blackbox: {
                    title: 'Giải thích các thành phần trong Blackbox',
                    intro: 'Blackbox là lớp giám sát, hiển thị minh bạch các giá trị toán học và dữ liệu trung gian trong quá trình thực thi giao thức bảo mật. Hover vào các thuật ngữ để xem giải thích ngắn.',
                    items: [
                        { icon: 'fa-key', name: 'Khóa công khai Alice', tooltip: 'Khóa công khai của Alice trong Diffie-Hellman (G^a mod P).', desc: 'Giá trị công khai được truyền qua kênh không an toàn để hai bên cùng suy ra Khóa gốc mà không làm lộ khóa riêng tư.' },
                        { icon: 'fa-key', name: 'Khóa công khai Bob', tooltip: 'Khóa công khai của Bob trong Diffie-Hellman (G^b mod P).', desc: 'Giá trị công khai của Bob dùng cho trao đổi khóa. Việc lộ khóa công khai không làm lộ khóa riêng tư.' },
                        { icon: 'fa-vault', name: 'Khóa gốc (Shared Secret)', tooltip: 'Bí mật chung (Shared Secret) suy ra từ Diffie-Hellman.', desc: 'Vật liệu khóa nền tảng để dẫn xuất khóa phiên và các lớp bảo mật kế tiếp.' },
                        { icon: 'fa-vault', name: 'Khóa phiên (256-bit)', tooltip: 'Khóa phiên 256-bit dùng cho AES, thường dẫn xuất từ Khóa gốc.', desc: 'Khóa đối xứng dùng để mã hóa/giải mã nội dung tin nhắn trong phiên hiện tại.' },
                        { icon: 'fa-random', name: 'Vector khởi tạo (IV)', tooltip: 'Vector khởi tạo ngẫu nhiên cho AES-CBC (mỗi tin nhắn).', desc: 'Đảm bảo bản mã khác nhau ngay cả khi bản rõ giống nhau; không cần bí mật nhưng phải ngẫu nhiên và không tái sử dụng theo đúng ngữ cảnh.' },
                        { icon: 'fa-random', name: 'Số ngẫu nhiên (Nonce)', tooltip: 'Giá trị ngẫu nhiên chỉ dùng một lần (Number used once).', desc: 'Tạo tính duy nhất/độ tươi trong dẫn xuất hoặc ghi dấu phiên, giúp giảm nguy cơ lặp mẫu.' },
                        { icon: 'fa-key', name: 'Khóa Vigenère', tooltip: 'Từ khóa dùng cho Vigenère.', desc: 'Từ khóa quyết định độ dịch chuyển ký tự theo vị trí bảng chữ cái; chỉ dùng cho mô phỏng mật mã cổ điển.' },
                        { icon: 'fa-file-lines', name: 'Bản rõ (Dữ liệu gốc)', tooltip: 'Nội dung gốc trước khi mã hóa.', desc: 'Dữ liệu người dùng nhập vào ở dạng đọc được trước khi đi qua lớp mã hóa.' },
                        { icon: 'fa-user-secret', name: 'Bản mã (Dữ liệu đã mã hóa)', tooltip: 'Dữ liệu sau mã hóa, có thể được đóng gói dạng Base64 để truyền/lưu.', desc: 'Dữ liệu đã được biến đổi bởi AES/Vigenère. Eve có thể nhìn thấy trên Firebase nhưng không đọc được nếu không có khóa.' },
                        { icon: 'fa-stamp', name: 'Mã xác thực toàn vẹn (HMAC)', tooltip: 'Chữ ký toàn vẹn (HMAC) tạo từ bản mã + khóa.', desc: 'Niêm phong chống sửa đổi: chỉ cần thay đổi 1 bit trong bản mã, kiểm tra tại Bob sẽ thất bại và hệ thống cảnh báo.' },
                        { icon: 'fa-link', name: 'Liên kết giả mạo', tooltip: 'Điểm kích hoạt tấn công Phishing.', desc: 'Khi người dùng nhấp vào liên kết độc hại, kẻ tấn công có thể thao túng giao diện (UI Hijacking) để chiếm quyền truy cập mà không cần bẻ khóa thuật toán.' },
                        { icon: 'fa-code', name: 'Định dạng Base64', tooltip: 'Cách đóng gói dữ liệu để truyền/lưu trữ.', desc: 'Base64 không phải là “mã hóa”. Đây chỉ là encoding để biểu diễn dữ liệu nhị phân ở dạng văn bản khi lưu trên Firebase hoặc truyền qua mạng.' }
                    ]
                },
                vulnerability: {
                    title: 'Phân tích lỗ hổng (Eve’s Scenario)',
                    body: 'Eve không bẻ gãy thuật toán mã hóa mà chiếm quyền thông qua <strong>liên kết giả mạo (Phishing)</strong>. Khi người dùng tương tác với link độc hại, hệ thống bảo mật bị thao túng từ tầng giao diện thông qua <strong>UI Hijacking</strong>, dẫn đến chiếm quyền truy cập.',
                    diagram: { type: 'vulnerability' }
                },
                techStack: {
                    title: 'Công nghệ sử dụng',
                    items: [
                        { label: 'Cryptographic Engine', value: 'CryptoJS (AES-256, SHA-256, HMAC).' },
                        { label: 'Database', value: 'Firebase Realtime Database (mô phỏng kênh truyền và lưu trữ tạm thời).' },
                        { label: 'Giao diện', value: 'HTML5, CSS3 (Grid/Flexbox), JavaScript ES6+.' },
                        { label: 'Simulation Logic', value: 'Ghi đè hàm (Function Overriding) để mô phỏng lỗ hổng tầng ứng dụng.' }
                    ]
                }
            }
        },
        en: {
            kicker: { icon: 'fa-microchip', text: 'Project' },
            title: {
                icon: 'fa-shield-heart',
                text: 'MULTI-LAYERED CRYPTOGRAPHIC PROTOCOL SIMULATION AND APPLICATION-LAYER VULNERABILITY ANALYSIS'
            },
            intro: [
                'This project experimentally simulates modern <strong>cryptographic standards</strong> in an <strong>End-to-End Encrypted (E2EE)</strong> messaging environment. It focuses on <strong>secure key establishment</strong>, <strong>block cipher encryption</strong>, and <strong>integrity verification</strong>, while highlighting real-world security risks introduced by application-layer and <strong>session hijacking</strong> threats.'
            ],
            sections: {
                architectureTitle: 'SECURITY ARCHITECTURE AND MECHANISMS',
                accordion: [
                    {
                        icon: 'fa-exchange-alt',
                        title: 'Diffie-Hellman (Key Exchange)',
                        body: [
                            'The system uses <strong>Diffie-Hellman</strong> to establish a <strong>shared secret</strong> between Alice and Bob without directly transmitting the secret over an insecure channel.',
                            'Initialization uses <strong>(P, G) = (23, 5)</strong>. Each party generates a private value, computes a public value, exchanges public keys, and derives the same shared secret as the basis for the session key.'
                        ],
                        tech: ['P = 23', 'G = 5'],
                        diagram: { type: 'dh' }
                    },
                    {
                        icon: 'fa-lock',
                        title: 'AES-256-CBC (Modern Block Cipher)',
                        body: [
                            '<strong>AES-256</strong> protects message content using symmetric encryption.',
                            '<strong>CBC (Cipher Block Chaining)</strong> mode chains blocks via XOR with the previous ciphertext block and uses a <strong>random IV</strong> to ensure ciphertext uniqueness even for identical plaintext inputs.'
                        ],
                        tech: ['256-bit', 'CBC', 'IV'],
                        diagram: { type: 'aes' }
                    },
                    {
                        icon: 'fa-key',
                        title: 'Vigenère (Classical Cipher)',
                        body: [
                            '<strong>Vigenère</strong> is implemented as a baseline for comparison to illustrate the evolution of cryptography.',
                            'It relies on a <strong>keyword-based</strong> polyalphabetic substitution, but is vulnerable to <strong>frequency analysis</strong> and is not suitable for modern security.'
                        ],
                        tech: ['Keyword', 'Polyalphabetic'],
                        diagram: { type: 'vig', keyword: 'VIGENERE' }
                    },
                    {
                        icon: 'fa-shield-alt',
                        title: 'HMAC-SHA256 (Authentication & Integrity)',
                        body: [
                            '<strong>HMAC</strong> detects tampering during transit by generating a <strong>signature</strong> from ciphertext and the session key.',
                            'If Eve modifies ciphertext, verification fails on the receiver side and the system raises an <strong>integrity alert</strong>.'
                        ],
                        tech: ['HMAC', 'SHA-256'],
                        diagram: { type: 'hmac' }
                    }
                ],
                dataJourney: {
                    title: 'Animated Data Journey',
                    subtitle: 'Alice (Sender) ➔ [Vault] ➔ Firebase ➔ Bob (Receiver)',
                    nodes: [
                        { className: 'dj-alice', icon: 'fa-paper-plane', label: 'Alice', sub: '(Sender)' },
                        { className: 'dj-vault', icon: 'fa-lock', label: 'Vault', sub: 'Encrypt + HMAC' },
                        { className: 'dj-firebase', icon: 'fa-cloud', label: 'Firebase', sub: 'Transport', showEve: true },
                        { className: 'dj-bob', icon: 'fa-inbox', label: 'Bob', sub: '(Receiver)' }
                    ]
                },
                blackbox: {
                    title: 'The Blackbox Terminology',
                    intro: 'The Blackbox acts as a Monitoring Layer, exposing intermediate values for educational purposes. Hover over technical terms to see short explanations.',
                    items: [
                        { icon: 'fa-key', name: 'Alice Pub', tooltip: 'Alice public value in Diffie-Hellman (G^a mod P).', desc: 'Transmitted openly to enable shared-secret derivation without exposing Alice’s private key.' },
                        { icon: 'fa-key', name: 'Bob Pub', tooltip: 'Bob public value in Diffie-Hellman (G^b mod P).', desc: 'Bob’s public counterpart used in the exchange; disclosure does not reveal the private key.' },
                        { icon: 'fa-vault', name: 'Root Key', tooltip: 'Shared secret derived from Diffie-Hellman.', desc: 'Root key material used to derive subsequent session keys and integrity primitives.' },
                        { icon: 'fa-vault', name: 'Session Key', tooltip: '256-bit session key for AES, typically derived from Root Key.', desc: 'Symmetric key used to encrypt/decrypt message content for the current session.' },
                        { icon: 'fa-random', name: 'Initialization Vector (IV)', tooltip: 'Random initialization vector per AES-CBC message.', desc: 'Ensures ciphertext uniqueness even when plaintext repeats; must be random and not reused in the same context.' },
                        { icon: 'fa-random', name: 'Nonce', tooltip: 'A number used once to strengthen uniqueness.', desc: 'Adds freshness/uniqueness to derivation or session-marking steps to reduce reuse patterns.' },
                        { icon: 'fa-key', name: 'Vigenère Key', tooltip: 'Keyword for the Vigenère cipher.', desc: 'Determines per-character shifts in the polyalphabetic substitution; included for classical-crypto comparison.' },
                        { icon: 'fa-file-lines', name: 'Plaintext', tooltip: 'Original message content before encryption.', desc: 'User input in readable form prior to cryptographic processing.' },
                        { icon: 'fa-user-secret', name: 'Ciphertext (Base64)', tooltip: 'Encrypted output, commonly encoded as Base64 for transport/storage.', desc: 'What travels through Firebase. Eve can see it, but cannot read it without the key.' },
                        { icon: 'fa-stamp', name: 'HMAC Signature', tooltip: 'Integrity tag computed from ciphertext + key.', desc: 'Tamper-evident seal: any modification breaks verification and triggers an integrity alert.' },
                        { icon: 'fa-link', name: 'Phishing Link', tooltip: 'Attack trigger via social engineering.', desc: 'Once the user clicks a malicious link, the attacker can compromise the UI (UI Hijacking) without breaking the encryption algorithm.' },
                        { icon: 'fa-code', name: 'Base64 Encoding', tooltip: 'Transport/storage encoding format.', desc: 'Base64 is not encryption. It is an encoding used to represent binary data as text for transmission and storage.' }
                    ]
                },
                vulnerability: {
                    title: 'Vulnerability Analysis (Eve’s Scenario)',
                    body: 'Eve gains access via a <strong>phishing link</strong>. Upon user interaction, the security system is compromised through <strong>UI Hijacking</strong> rather than breaking the encryption algorithm.',
                    diagram: { type: 'vulnerability' }
                },
                techStack: {
                    title: 'Tech Stack',
                    items: [
                        { label: 'Cryptographic Engine', value: 'CryptoJS (AES-256, SHA-256, HMAC).' },
                        { label: 'Database', value: 'Firebase Realtime Database (simulated transport + temporary storage).' },
                        { label: 'Frontend', value: 'HTML5, CSS3 (Grid/Flexbox), JavaScript (ES6+).' },
                        { label: 'Simulation Logic', value: 'Function overriding to simulate application-layer vulnerabilities.' }
                    ]
                }
            }
        }
    };

    function escapeHtml(value) {
        return String(value)
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    function renderTechChips(chips) {
        if (!chips || !chips.length) return '';
        return `<div style="display:flex;flex-wrap:wrap;gap:.45rem;margin:.7rem 0 0;">
            ${chips.map(x => `<span class="crypto-code">${escapeHtml(x)}</span>`).join('')}
        </div>`;
    }

    const ARCH_DIAGRAM_CAPTIONS = {
        dh: { en: 'Public keys merge into a shared secret.', vi: 'Hai khóa công khai hòa trộn để tạo Khóa gốc.' },
        aes: { en: 'Data passes through encryption layers.', vi: 'Dữ liệu đi qua các lớp bảo mật mã hóa.' },
        vig: { en: 'Alphabet wheel shifts by keyword.', vi: 'Vòng xoay chữ cái dịch chuyển theo từ khóa.' },
        hmac: { en: 'Integrity stamp seals the ciphertext.', vi: 'Con dấu toàn vẹn đóng lên bản mã.' },
        vulnerability: { en: 'Eve hijacks UI via phishing link.', vi: 'Eve chiếm quyền UI qua liên kết giả mạo.' }
    };

    function renderArchitectureDiagram(diagram, lang) {
        if (!diagram || !diagram.type) return '';
        const isEn = lang === 'en';
        const cap = escapeHtml(ARCH_DIAGRAM_CAPTIONS[diagram.type]?.[isEn ? 'en' : 'vi'] || '');

        switch (diagram.type) {
            case 'vulnerability':
                return `
                <div class="arch-diagram vulnerability-diagram" aria-hidden="true" style="flex-direction:column;gap:1rem;">
                    <div style="display:flex;align-items:center;justify-content:center;gap:2rem;width:100%;">
                        <div class="vuln-actor vuln-eve">
                            <div class="vuln-icon"><i class="fas fa-user-secret"></i></div>
                            <div class="vuln-label">Eve</div>
                        </div>
                        <div class="vuln-link-flow">
                            <i class="fas fa-link"></i>
                        </div>
                        <div class="vuln-actor vuln-user">
                            <div class="vuln-icon"><i class="fas fa-user"></i></div>
                            <div class="vuln-label">${isEn ? 'User' : 'Người dùng'}</div>
                        </div>
                    </div>
                    <div class="arch-caption">${cap}</div>
                </div>`;
            case 'dh':
                return `
                <div class="arch-diagram dh-diagram" aria-hidden="true">
                    <div class="dh-person dh-alice">
                        <div class="dh-avatar"><i class="fas fa-user"></i></div>
                        <div class="dh-name">Alice</div>
                    </div>
                    <div class="dh-mid">
                        <div class="dh-frag dh-frag-a"><i class="fas fa-key"></i></div>
                        <div class="dh-frag dh-frag-b"><i class="fas fa-key"></i></div>
                        <div class="dh-shared"><i class="fas fa-key"></i></div>
                    </div>
                    <div class="dh-person dh-bob">
                        <div class="dh-avatar"><i class="fas fa-user"></i></div>
                        <div class="dh-name">Bob</div>
                    </div>
                    <div class="arch-caption">${cap}</div>
                </div>`;
            case 'aes':
                return `
                <div class="arch-diagram aes-diagram" aria-hidden="true">
                    <div class="aes-vault">
                        <div class="aes-vault-door">
                            <div class="aes-door-rings">
                                <span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span>
                                <span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span>
                                <span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span><span class="aes-ring"></span>
                                <span class="aes-ring"></span><span class="aes-ring"></span>
                            </div>
                            <div class="aes-lock"><i class="fas fa-vault"></i></div>
                        </div>
                    </div>
                    <div class="aes-msg aes-plain"><i class="fas fa-envelope"></i></div>
                    <div class="aes-msg aes-cipher"><i class="fas fa-cubes"></i></div>
                    <div class="arch-caption">${cap}</div>
                </div>`;
            case 'vig': {
                const keyword = (diagram.keyword || (isEn ? 'KEYWORD' : 'TUKHOA')).toString();
                const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                const normalized = keyword.replace(/[^A-Z]/g, '').toUpperCase();
                const firstChar = normalized[0] || 'A';
                const shift = Math.max(0, alphabet.indexOf(firstChar));
                const shiftPx = -shift * 8;
                return `
                <div class="arch-diagram vig-diagram" aria-hidden="true">
                    <div class="vig-row">
                        <div class="vig-label">${escapeHtml(isEn ? 'Original alphabet' : 'Bảng chữ cái gốc')}</div>
                        <div class="vig-alphabet">${alphabet}</div>
                    </div>
                    <div class="vig-cogline">
                        <div class="vig-cog"><i class="fas fa-cog"></i></div>
                        <div class="vig-keyword">${escapeHtml(isEn ? 'Keyword:' : 'Từ khóa:')} <span class="crypto-code">${escapeHtml(keyword)}</span></div>
                    </div>
                    <div class="vig-row" style="--vig-shift:${shiftPx}px;">
                        <div class="vig-label">${escapeHtml(isEn ? 'Shifted alphabet' : 'Bảng chữ cái đã dịch chuyển')}</div>
                        <div class="vig-alphabet vig-shift-track">
                            <span class="vig-shifted">${alphabet}${alphabet}</span>
                        </div>
                    </div>
                    <div class="arch-caption">${cap}</div>
                </div>`;
            }
            case 'hmac':
                return `
                <div class="arch-diagram hmac-diagram" aria-hidden="true">
                    <div class="hmac-doc">
                        <div class="hmac-box"><i class="fas fa-box"></i></div>
                        <div class="hmac-text"><i class="fas fa-user-secret"></i></div>
                    </div>
                    <div class="hmac-wax"><i class="fas fa-fingerprint"></i></div>
                    <div class="hmac-ok"><i class="fas fa-check"></i></div>
                    <div class="arch-caption">${cap}</div>
                </div>`;
            default:
                return '';
        }
    }

    function renderProject(data, lang) {
        const effectiveLang = lang === 'en' ? 'en' : 'vi';
        const s = data.sections;
        const accordion = s.accordion.map((item, idx) => {
            const title = `${idx + 1}. ${item.title}`;
            return `
                <details class="project-details" style="margin-bottom:25px;">
                    <summary class="details-summary"><i class="fas ${escapeHtml(item.icon)}"></i> ${escapeHtml(title)}</summary>
                    <div class="details-content">
                        ${item.body.map(p => `<p style="line-height:1.8;">${p}</p>`).join('')}
                        ${renderArchitectureDiagram(item.diagram, effectiveLang)}
                    </div>
                </details>`;
        }).join('');

        const blackboxItems = s.blackbox.items.map(it => `
            <div class="bb-row">
                <div class="bb-head">
                    <div class="bb-icon"><i class="fas ${escapeHtml(it.icon)}"></i></div>
                    <div class="bb-name"><strong>${escapeHtml(it.name)}</strong></div>
                </div>
                <div class="bb-body">${escapeHtml(it.desc)}</div>
            </div>
        `).join('');

        const techItems = s.techStack.items.map(it => `<li><strong>${escapeHtml(it.label)}:</strong> ${escapeHtml(it.value)}</li>`).join('');
        const isEn = effectiveLang === 'en';
        const journeyNodes = (s.dataJourney.nodes || []).map(node => `
            <div class="dj-node ${escapeHtml(node.className)}">
                <div class="dj-icon"><i class="fas ${escapeHtml(node.icon)}"></i></div>
                <div class="dj-label">${escapeHtml(node.label)}</div>
                <div class="dj-sub">${escapeHtml(node.sub)}</div>
                ${node.showEve ? `<div class="dj-eve" aria-hidden="true" title="${escapeHtml(isEn ? 'Intruder (Eve) — phishing trigger' : 'Kẻ nghe lén (Eve) — kích hoạt phishing')}"><i class="fas fa-eye"></i><i class="fas fa-link"></i><i class="fas fa-lock"></i></div>` : ``}
            </div>
        `).join('');

        return `
            <div class="team-kicker"><i class="fas ${escapeHtml(data.kicker.icon)}"></i> ${escapeHtml(data.kicker.text)}</div>
            <h2 style="color:#ffd8d8;margin-bottom:25px;display:flex;align-items:center;gap:.55rem;font-size:1.48rem;text-transform:uppercase;letter-spacing:0.07em;">
                <i class="fas ${escapeHtml(data.title.icon)}" style="color:#f85149;"></i>
                ${escapeHtml(data.title.text)}
            </h2>
            ${data.intro.map(p => `<p style="line-height:1.8;opacity:.95;color:#f5f7ff;margin-bottom:25px;">${p}</p>`).join('')}
            <h3 style="color:#ffd8d8;margin-bottom:20px;font-size:1.2rem;border-left:4px solid #f85149;padding-left:12px;">${escapeHtml(s.architectureTitle)}</h3>
            ${accordion}

            <div class="data-journey">
                <h3 style="color:#ffd8d8;margin:0 0 .55rem;font-size:1.1rem;display:flex;align-items:center;gap:.5rem;">
                    <i class="fas fa-route" style="color:#f85149;"></i> ${escapeHtml(s.dataJourney.title)}
                </h3>
                <p style="margin:.2rem 0 1.3rem;color:#d9e7ff;opacity:.9;line-height:1.8;text-align:center;">${escapeHtml(s.dataJourney.subtitle)}</p>
                <div class="dj-stage" role="img" aria-label="${escapeHtml(s.dataJourney.subtitle)}">
                    ${journeyNodes}
                    <i class="fas fa-key dj-key" aria-hidden="true"></i>
                    <i class="fas fa-envelope dj-envelope" aria-hidden="true"></i>
                </div>
            </div>

            <details class="project-details" style="margin-bottom:25px;">
                <summary class="details-summary"><i class="fas fa-box"></i> ${escapeHtml(s.blackbox.title)}</summary>
                <div class="details-content">
                    <p style="line-height:1.8;margin:0 0 1rem;color:#d9e7ff;">${escapeHtml(s.blackbox.intro)}</p>
                    <div class="blackbox-grid">${blackboxItems}</div>
                </div>
            </details>

            <div class="project-highlight" style="line-height:1.7;margin-bottom:25px;">
                <h4 style="margin-bottom:15px;"><i class="fas fa-user-secret"></i> ${escapeHtml(s.vulnerability.title)}</h4>
                <p style="line-height:1.8;margin:0;">${s.vulnerability.body}</p>
                ${renderArchitectureDiagram(s.vulnerability.diagram, effectiveLang)}
            </div>

            <div class="project-highlight" style="line-height:1.7;margin-bottom:25px;">
                <h4 style="margin-bottom:15px;"><i class="fas fa-cogs"></i> ${escapeHtml(s.techStack.title)}</h4>
                <ul style="margin:0;padding-left:1.2rem;line-height:1.7;">${techItems}</ul>
            </div>
        `;
    }

    function updateContent() {
        const root = document.getElementById('projectRoot');
        if (!root) return;
        const lang = currentLang === 'en' ? 'en' : 'vi';
        const data = projectData[lang] || projectData.vi;
        root.innerHTML = renderProject(data, lang);
    }

    window.toggleLanguage = function() {
        currentLang = currentLang === 'vi' ? 'en' : 'vi';
        applyTranslations();
        // Update language label
        const langLabel = document.getElementById('langLabel');
        if (langLabel) {
            langLabel.textContent = currentLang === 'en' ? 'ENG' : 'VN';
        }
    };

    function homeHistoryUpdateReactions(ts, reactions) {
        const arr = homeHistoryGetAll();
        const item = arr.find(x => x.ts === ts);
        if (item) {
            item.reactions = reactions;
            homeHistorySave(arr);
        }
    }

    /* ================================================================
    THEME TOGGLE — dark / light
    ================================================================ */
    // Default to light mode
    document.body.classList.add('light-mode');

    window.toggleUtilityHub = function(event) {
        if (event) event.stopPropagation();
        const hubExpanded = document.getElementById('hubExpanded');
        if (hubExpanded) {
            const isOpen = hubExpanded.classList.contains('show');
            if (isOpen) {
                hubExpanded.classList.remove('show');
                document.removeEventListener('click', closeUtilityHub);
            } else {
                hubExpanded.classList.add('show');
                setTimeout(() => {
                    document.addEventListener('click', closeUtilityHub);
                }, 100);
            }
        }
    };

    function closeUtilityHub(event) {
        const hub = document.querySelector('.utility-hub');
        if (hub && !hub.contains(event.target)) {
            const hubExpanded = document.getElementById('hubExpanded');
            if (hubExpanded) {
                hubExpanded.classList.remove('show');
                document.removeEventListener('click', closeUtilityHub);
            }
        }
    }

    window.toggleTheme = function() {
        const isDark = document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode', !isDark);
        const icon = document.getElementById('themeIcon');
        if (icon) {
            icon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
        }
        // Call applyTranslations to update all labels with correct language
        applyTranslations();
    };

    /* ================================================================
    INIT
    ================================================================ */
    // Initialize language and theme labels
    window.addEventListener('load', function() {
        const langLabel = document.getElementById('langLabel');
        if (langLabel) {
            langLabel.textContent = currentLang === 'en' ? 'ENG' : 'VN';
        }
    });

    // ===== THÊM TÍNH NĂNG ENTER ĐỂ GỬI =====
const aliceInput = document.getElementById('aliceInput');
const bobInput = document.getElementById('bobInput');
const friendInput = document.getElementById('friendInput');

if (aliceInput) {
    aliceInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendData('Alice');
        }
    });
}
if (bobInput) {
    bobInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendData('Bob');
        }
    });
}
if (friendInput) {
    friendInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendFriendMessage();
        }
    });
}

    // Count stats for friend messages
    const _origSendFriendMsg = window.sendFriendMessage;
    window.sendFriendMessage = function() {
        const inp = document.getElementById('friendInput');
        const msg = inp?.value?.trim();
        const hasImg = pendingImages.friend && pendingImages.friend.length > 0;
        if (msg) localStorage.setItem('stat_msg', (parseInt(localStorage.getItem('stat_msg')||'0') + 1).toString());
        if (hasImg) localStorage.setItem('stat_img', (parseInt(localStorage.getItem('stat_img')||'0') + pendingImages.friend.length).toString());
        _origSendFriendMsg();
        if (msg || hasImg) showToast(t('messageSent'), 1800);
    };
    updateRootKeyUI();
    loadAccountInfo();
    (function initAuthCodeStream() {
        const el = document.getElementById('authCodeStream');
        if (!el) return;
        function getAuthFeed() {
            return [
                t('bootMessage'),
                t('cryptoDHMessage'),
                t('cryptoAESMessage'),
                t('verifyIntegrityMessage'),
                t('threatSimLoaded')
            ];
        }
        let feedIdx = 0;
        setInterval(() => {
            const authFeed = getAuthFeed();
            feedIdx = (feedIdx + 1) % authFeed.length;
            el.textContent = authFeed.slice(feedIdx).concat(authFeed.slice(0, feedIdx)).join('\n');
        }, 1150);
    })();
    applyTeamMemberAvatars();
    setupTeamMemberClickHandlers();
    transparentizeLogoBackground();
    updateAuthUI();
    applyTranslations();
    restoreHomeHistory();   // reload Alice↔Bob chat history from localStorage
    restoreConsoleLog();    // reload blackbox console from localStorage
    switchPage('project');

    /* ================================================================
    FLOATING PARTICLES
    ================================================================ */
    (function initParticles() {
        const canvas = document.getElementById('particles-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let particles = [];
        let W, H;

        function resize() {
            W = canvas.width  = window.innerWidth;
            H = canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);

        class Particle {
            constructor() { this.reset(true); }
            reset(initial) {
                this.x = Math.random() * W;
                this.y = initial ? Math.random() * H : H + 10;
                this.r = Math.random() * 1.8 + .5;
                this.vx = (Math.random() - .5) * .35;
                this.vy = -(Math.random() * .55 + .15);
                this.alpha = Math.random() * .4 + .1;
                this.color = Math.random() > .5 ? `rgba(176,28,45,${this.alpha})` : `rgba(255,255,255,${this.alpha * .5})`;
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                if (this.y < -10) this.reset(false);
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.fill();
            }
        }

        for (let i = 0; i < 55; i++) particles.push(new Particle());

        function loop() {
            ctx.clearRect(0, 0, W, H);
            particles.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(loop);
        }
        loop();
    })();

    /* ================================================================
    ACCOUNT — STATS COUNTER
    ================================================================ */
    function updateAccountStats() {
        let msgCount = parseInt(localStorage.getItem('stat_msg') || '0');
        let imgCount = parseInt(localStorage.getItem('stat_img') || '0');
        const encCount = parseInt(localStorage.getItem('stat_enc') || '0');
        const m = document.getElementById('statMsgCount');
        const i = document.getElementById('statImgCount');
        const e = document.getElementById('statEncCount');
        if (m) animateCount(m, msgCount);
        if (i) animateCount(i, imgCount);
        if (e) animateCount(e, encCount);
    }

    function animateCount(el, target) {
        let cur = 0;
        const step = Math.max(1, Math.ceil(target / 30));
        const timer = setInterval(() => {
            cur = Math.min(cur + step, target);
            el.textContent = cur;
            if (cur >= target) clearInterval(timer);
        }, 30);
    }

    // Hook into sendData to count stats
    const _origSendData = window.sendData;
    window.sendData = function(sender) {
        const who = sender === 'Alice' ? 'alice' : 'bob';
        if (pendingImages[who] && pendingImages[who].length > 0) {
            localStorage.setItem('stat_img', (parseInt(localStorage.getItem('stat_img')||'0') + pendingImages[who].length).toString());
        }
        const inputId = sender === 'Alice' ? 'aliceInput' : 'bobInput';
        const msg = document.getElementById(inputId).value;
        if (msg.trim()) {
            localStorage.setItem('stat_msg', (parseInt(localStorage.getItem('stat_msg')||'0') + 1).toString());
            localStorage.setItem('stat_enc', (parseInt(localStorage.getItem('stat_enc')||'0') + 1).toString());
        }
        _origSendData(sender);
    };

    /* ================================================================
    ACCOUNT — CHANGE AVATAR
    ================================================================ */
    function setAliceAvatarSrc(src) {
        document.querySelectorAll('img[alt="Alice"]').forEach(img => img.src = src);
        localStorage.setItem('avatarAlice', src);
    }
    function handleAliceAvatarFile(file) {
        if (!file || !file.type || !file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = e => {
            setAliceAvatarSrc(e.target.result);
            showToast(t('avatarUpdateSuccess'));
        };
        reader.readAsDataURL(file);
    }
    window.changeAvatar = function(input) {
        const file = input.files[0];
        if (!file) return;
        handleAliceAvatarFile(file);
    };

    // Restore saved avatar
    const savedAvatar = localStorage.getItem('avatarAlice');
    if (savedAvatar) setAliceAvatarSrc(savedAvatar);
    const aliceDrop = document.getElementById('aliceAvatarDropZone');
    if (aliceDrop) {
        aliceDrop.addEventListener('dragover', e => {
            e.preventDefault();
            aliceDrop.style.filter = 'drop-shadow(0 0 10px rgba(117,185,230,.6))';
        });
        aliceDrop.addEventListener('dragleave', () => {
            aliceDrop.style.filter = '';
        });
        aliceDrop.addEventListener('drop', e => {
            e.preventDefault();
            aliceDrop.style.filter = '';
            const file = e.dataTransfer?.files?.[0];
            if (file) handleAliceAvatarFile(file);
        });
    }

    // Override switchPage to load stats
    const _origSwitch = window.switchPage;
    window.switchPage = function(page, event) {
        _origSwitch(page, event);
        if (page === 'account') {
            updateAccountStats();
            // Update display name/email
            const n = localStorage.getItem('accountName');
            const dn = document.getElementById('accDisplayName');
            if (dn && n) dn.innerHTML = `<i class="fas fa-cloud"></i> ${n}`;
            const em = localStorage.getItem('accountEmail');
            const de = document.getElementById('accDisplayEmail');
            if (de && em) de.textContent = em;
        }
    };

    // (theme color picker removed)

    /* ================================================================
    TOAST NOTIFICATION
    ================================================================ */
    window.showToast = function(msg, duration = 2800) {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = msg;
        container.appendChild(toast);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => toast.classList.add('show'));
        });
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };

    /* ================================================================
    HACK SCENARIO: SYSTEM-WIDE ACCOUNT TAKEOVER (XSS)
    ================================================================ */

    window.triggerXSSAttack = function() {
        showToast(t('hackerInject'), 3000);
        
        // If tour is running, we might want to handle it, but here we assume it's triggered via triggerHackScenario
        const container = document.getElementById('aliceOutput');
        if (!container) return;
        
        const div = document.createElement('div');
        div.className = 'bubble friend';
        div.style.border = "2px dashed #ff5252";
        div.style.backgroundColor = "rgba(255, 82, 82, 0.1)";

        const time = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });

        div.innerHTML = `
            <strong style="color:#ff5252;"><i class="fas fa-exclamation-triangle"></i> [${t('hackerAlertTitle')}]</strong><br>
            ${t('hackerAlertBody')} <b style="color:#2563eb; cursor:pointer; text-decoration:underline; font-size:1.1rem;" onclick="showFakePasswordPrompt()">[HERE]</b> ${t('hackerAlertLink')}
            <span class="timestamp"><i class="far fa-clock"></i> ${time}</span>
            <br><span style="font-size:0.6rem; color:#75b9e6; margin-top:5px; display:block; font-weight:bold;">✅ INTACT (Valid System Signature)</span>
        `;

        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
    };

    window.showFakePasswordPrompt = function() {
        document.getElementById('xssModal').classList.add('show');
    };

    window.executeAccountTakeover = function() {
        const pwd = document.getElementById('xssPassword').value.trim();
        if(!pwd) {
            showToast(t('pwdRequired'));
            return;
        }

        document.getElementById('xssModal').classList.remove('show');
        window.isSystemHacked = true;

        const log = document.getElementById('processLog');
        if(log) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.style.borderColor = '#ff5252';
            entry.style.background = 'rgba(255, 82, 82, 0.1)';
            const timeStr = new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit', second:'2-digit' });
            entry.innerHTML = `
                <div class="log-header">
                    <span class="log-badge" style="background:#4a0d17;border-color:#8b1a28;color:#ff5252;">
                        <i class="fas fa-skull"></i> ACCOUNT TAKEOVER (ATO)
                    </span>
                    <span style="color:#ff5252;font-size:.68rem;"><i class="far fa-clock"></i> ${timeStr}</span>
                </div>
                <div class="log-row">
                    <span class="log-label" style="color:#ff5252; width: 100px;">Tactic</span>
                    <span class="log-value" style="color:#ff5252; background:transparent; border:none; padding:0;">XSS Payload / Session Hijack</span>
                </div>
                <div class="log-row">
                    <span class="log-label" style="color:#ff5252; width: 100px;"><i class="fas fa-key"></i> Password</span>
                    <span class="log-value" style="font-weight:900; background:#ff5252; color:white; font-size:1rem; padding: 4px 10px;">${pwd}</span>
                </div>
                <div class="log-row">
                    <span class="log-label" style="color:#ff5252; width: 100px;">Result</span>
                    <span class="integrity-badge" style="border-color:#ff5252;color:#ff5252;">🚨 ALICE COMPROMISED</span>
                </div>`;
            log.prepend(entry);
        }

        const hackerAvatar = 'https://api.dicebear.com/7.x/bottts/svg?seed=Hacker&backgroundColor=ff0000';
        const nameHacked = t('hackedName');
        const txtCompromised = t('compromised');
        const txtLocked = t('accLocked');
        const txtBreached = t('sysBreached');

        // --- 1. Deface Home Page ---
        document.querySelectorAll('.column.alice .chat-header h4').forEach(h => {
            h.innerHTML = `<i class="fas fa-skull" style="color:#ff5252;"></i> <span style="color:#ff5252; font-weight:bold;">${nameHacked}</span>`;
        });
        document.querySelectorAll('.column.alice .avatar, .column.alice .avatar-wrap img').forEach(a => {
            a.src = hackerAvatar; a.style.borderColor = '#ff5252'; a.style.boxShadow = '0 0 20px #ff5252';
        });
        document.querySelectorAll('.column.alice .status-pill').forEach(s => {
            s.innerHTML = `<span class="status-dot" style="background:#ff5252; box-shadow: 0 0 10px #ff5252; animation: none;"></span> <span style="color:#ff5252; font-weight:bold;">${txtCompromised}</span>`;
            s.style.borderColor = '#ff5252'; s.style.background = 'rgba(255,0,0,0.1)';
        });
        const aliceInput = document.getElementById('aliceInput');
        if(aliceInput) {
            aliceInput.disabled = true; aliceInput.value = ""; aliceInput.placeholder = txtLocked;
            aliceInput.style.color = "#ff5252"; aliceInput.style.fontWeight = "bold";
        }
        const aliceSendBtn = document.querySelector('.column.alice .send-btn');
        if(aliceSendBtn) { aliceSendBtn.disabled = true; aliceSendBtn.style.background = "#555"; }
        

        // --- 2. Deface Friends Page ---
        const friendInput = document.getElementById('friendInput');
        if(friendInput) {
            friendInput.disabled = true; friendInput.value = ""; friendInput.placeholder = txtLocked;
            friendInput.style.color = "#ff5252"; friendInput.style.fontWeight = "bold";
        }
        const friendSendBtn = document.querySelector('#page-friends .send-btn');
        if(friendSendBtn) { friendSendBtn.disabled = true; friendSendBtn.style.background = "#555"; }

        // --- 3. Deface Account Page ---
        const accName = document.getElementById('accDisplayName');
        if(accName) accName.innerHTML = `<i class="fas fa-skull" style="color:#ff5252;"></i> <span style="color:#ff5252; font-weight:bold;">${nameHacked}</span>`;
        const accEmail = document.getElementById('accDisplayEmail');
        if(accEmail) { accEmail.textContent = "hacker@eve.darkweb"; accEmail.style.color = "#ff5252"; }
        const accAvatar = document.querySelector('.account-avatar');
        if(accAvatar) { accAvatar.src = hackerAvatar; accAvatar.style.borderColor = '#ff5252'; accAvatar.style.boxShadow = '0 0 20px #ff5252'; }
        
        const inputName = document.getElementById('inputName');
        if(inputName) { inputName.value = nameHacked; inputName.disabled = true; inputName.style.color = "#ff5252"; inputName.style.fontWeight = "bold"; }
        const inputEmail = document.getElementById('inputEmail');
        if(inputEmail) { inputEmail.value = "hacker@eve.darkweb"; inputEmail.disabled = true; inputEmail.style.color = "#ff5252"; inputEmail.style.fontWeight = "bold"; }
        const saveBtn = document.querySelector('.save-btn');
        if(saveBtn) { saveBtn.disabled = true; saveBtn.style.background = "#555"; saveBtn.innerHTML = '<i class="fas fa-lock"></i> LOCKED'; }

        // --- 4. Deface Global Topbar ---
        const brandSpan = document.querySelector('.brand span');
        if(brandSpan) brandSpan.innerHTML = `<span style="color:#ff5252; font-weight:bold;"><i class="fas fa-biohazard"></i> ${txtBreached}</span>`;
        const authLabel = document.getElementById('authLabel');
        if(authLabel) { authLabel.textContent = "COMPROMISED"; authLabel.style.color = "#ff5252"; }
        const authBtnIcon = document.querySelector('#authToggleBtn i');
        if(authBtnIcon) { authBtnIcon.className = "fas fa-skull"; authBtnIcon.style.color = "#ff5252"; }

        showToast(t('takeoverSuccess'), 5000);
    };

    const _origHackedSwitchPage = window.switchPage;
    window.switchPage = function(page, event) {
        _origHackedSwitchPage(page, event);
        if (window.isSystemHacked) {
            const nameHacked = t('hackedName');
            const inputName = document.getElementById('inputName');
            if(inputName) { inputName.value = nameHacked; inputName.style.color = "#ff5252"; }
            const inputEmail = document.getElementById('inputEmail');
            if(inputEmail) { inputEmail.value = "hacker@eve.darkweb"; inputEmail.style.color = "#ff5252"; }
            const accName = document.getElementById('accDisplayName');
            if(accName) accName.innerHTML = `<i class="fas fa-skull" style="color:#ff5252;"></i> <span style="color:#ff5252; font-weight:bold;">${nameHacked}</span>`;
            
            // Cập nhật triệt để Email còn sót lại
            const accEmail = document.getElementById('accDisplayEmail');
            if(accEmail) { accEmail.textContent = "hacker@eve.darkweb"; accEmail.style.color = "#ff5252"; }
        }
    };

    /* ================================================================
    SEND TOAST on message sent
    ================================================================ */
    const _origSendDataFinal = window.sendData;
    window.sendData = function(sender) {
        const inputId = sender === 'Alice' ? 'aliceInput' : 'bobInput';
        const msg = document.getElementById(inputId)?.value?.trim();
        const who = sender.toLowerCase();
        const hasImg = pendingImages[who] && pendingImages[who].length > 0;
        _origSendDataFinal(sender);
        if (msg || hasImg) {
            const label = hasImg && !msg ? '📷 Ảnh đã gửi!' : '🔐 Tin nhắn đã mã hoá & gửi!';
            showToast(label, 2200);
        }
    };
    /* ================================================================
    KHÓA TRIỆT ĐỂ: CHẶN ALICE THẢ TIM VÀ XÓA CHAT KHI BỊ HACK
    ================================================================ */
    
    // 1. Chặn chức năng Thả tim (Chỉ chặn phía Alice và trang Bạn bè)
    const _origAddReaction = window.addReaction;
    window.addReaction = function(emoji) {
        if (window.isSystemHacked) {
            const target = window.event ? window.event.target : null;
            // Nếu click phát sinh từ cột của Alice hoặc trang Bạn bè thì chặn lại!
            if (target && (target.closest('.column.alice') || target.closest('#page-friends'))) {
                showToast(t('accLocked'), 2000);
                return; 
            }
        }
        _origAddReaction(emoji); // Nếu là Bob bấm thì vẫn cho chạy bình thường
    };

    // 2. Chặn chức năng Xóa lịch sử chat ở trang Chủ
    const _origClearHomeChat = window.clearHomeChat;
    window.clearHomeChat = function() {
        if (window.isSystemHacked) {
            const target = window.event ? window.event.target : null;
            if (target && target.closest('.column.alice')) {
                showToast(t('accLocked'), 2000);
                return;
            }
        }
        _origClearHomeChat();
    };

    // 3. Chặn chức năng Xóa lịch sử chat ở trang Bạn bè
    const _origClearFriendHistory = window.clearFriendHistory;
    window.clearFriendHistory = function() {
        if (window.isSystemHacked) {
            showToast(t('accLocked'), 2000);
            return;
        }
        _origClearFriendHistory();
    };

    // 4. Chặn chức năng Xóa từng người bạn
    const _origDeleteFriendMessages = window.deleteFriendMessages;
    window.deleteFriendMessages = function(name, event) {
        if (window.isSystemHacked) {
            showToast(t('accLocked'), 2000);
            if (event) event.stopPropagation();
            return;
        }
        _origDeleteFriendMessages(name, event);
    };
    // ================================================================
    // CHẶN ĐĂNG NHẬP LẠI SAU KHI BỊ HACK
    // ================================================================
    const _origSubmitAliceLogin = window.submitAliceLogin;
    window.submitAliceLogin = function() {
        // Nếu hệ thống đã bị Eve chiếm quyền
        if (window.isSystemHacked) {
            // 1. Hiện thông báo tàn nhẫn
            const errorMsg = currentLang === 'vi' 
                ? '❌ Đăng nhập thất bại! Mật khẩu đã bị thay đổi cách đây ít phút.' 
                : '❌ Login failed! Password was recently changed.';
            showToast(errorMsg, 4500);
            
            // 2. Hiệu ứng rung lắc (Shake) khung đăng nhập để từ chối
            const authCard = document.querySelector('.auth-card');
            if (authCard) {
                authCard.style.transition = 'transform 0.05s';
                authCard.style.transform = 'translateX(-10px)';
                setTimeout(() => authCard.style.transform = 'translateX(10px)', 50);
                setTimeout(() => authCard.style.transform = 'translateX(-10px)', 100);
                setTimeout(() => authCard.style.transform = 'translateX(10px)', 150);
                setTimeout(() => authCard.style.transform = 'translateX(0)', 200);
            }
            
            // 3. Khóa chết, tuyệt đối không gọi hàm đăng nhập gốc!
            return; 
        }
        
        // Nếu chưa bị hack thì cho đăng nhập bình thường
        _origSubmitAliceLogin();
    };
    
    /* ================================================================
    TOUR SHOWCASE CONFIG & LOGIC
    ================================================================ */
    const tourConfig = {
        vi: {
            login_title: "Chào mừng bạn!",
            login_desc: "Chào mừng bạn đến với Secure Messenger. Hãy đăng nhập để trải nghiệm không gian trò chuyện bảo mật cấp độ quân đội.",
            header_title: "Thanh Header",
            header_desc: "Nơi chứa logo, chuyển đổi ngôn ngữ (EN/VI) và chế độ Sáng/Tối giúp tối ưu trải nghiệm người dùng.",
            nav_title: "Menu Dự án & Đội ngũ",
            nav_desc: "Tìm hiểu về mục tiêu nghiên cứu bảo mật và thông tin các thành viên phát triển.",
            account_title: "Quản lý Tài khoản",
            account_desc: "Nơi quản lý thông tin cá nhân và đăng xuất an toàn.",
            sidebar_title: "Danh sách Bạn bè",
            sidebar_desc: "Quản lý các cuộc hội thoại, xem trạng thái online. Bạn có thể di chuột để hiện nút xóa chat.",
            chatbox_title: "Khung Chat Bảo Mật",
            chatbox_desc: "Ô nhập tin nhắn, gửi ảnh và các nút chức năng hỗ trợ mã hóa E2E.",
            confirm_title: "Giai đoạn 1 Hoàn tất!",
            confirm_desc: "Bạn đã nắm rõ cách dùng cơ bản. Bạn có muốn xem demo tính năng Hack và Gửi tin nhắn bảo mật không?",
            confirm_yes: "CÓ, XEM TIẾP",
            confirm_no: "ĐỂ SAU",
            hacked_final_title: "SECURITY ALERT",
            hacked_final_desc: "System compromised via password vulnerability. Be careful with Phishing attacks!",
            exit_btn: "EXIT TOUR"
        },
        en: {
            login_title: "Welcome to Secure Messenger!",
            login_desc: "Welcome to Secure Messenger. Please login to experience military-grade secure messaging.",
            login_btn: "Start Tour",
            welcome_title: "Welcome to Secure Messenger!",
            welcome_desc: "Military-grade encrypted messaging system. This tour will guide you through key features.",
            // Step 1: Personal Setup
            setup_title: "Personal Setup",
            setup_desc: "Welcome! First, choose your preferred language (English/Vietnamese) and switch between Light/Dark mode for the most comfortable visual experience.",
            // Step 2: Explore System Information
            project_title: "Explore System Information",
            project_desc: "Want to know how this system was built? Click 'Project' to see details about the technology and goals of Secure Messenger.",
            // Step 3: Meet the Team
            team_title: "Meet the Team",
            team_desc: "Here you can find information about the people who developed this application.",
            // Step 4: Manage Connections
            friends_title: "Manage Connections",
            friends_desc: "This is where you manage your contact list. You can search and connect with other users here before starting conversations.",
            // Step 5: Experience Secure Messaging
            chat_title: "Experience Secure Messaging",
            chat_desc: "Finally, let's return to Home. This is the main interface for sending and receiving secure messages. Try selecting a friend and sending 'Hello' to experience the system's speed!",
            lang_title: "Language Switch",
            lang_desc: "Flexible switching between ENG/VIET for all Data Science & Cryptography terms.",
            theme_title: "Display Mode",
            theme_desc: "UI optimized for both developers and end-users.",
            team_desc: "Info about Dinh Ky Vi, Nguyen Duy Bao Tran, Nguyen Bui Minh Hang and their roles.",
            alice_title: "Alice & Bob Demo",
            alice_desc: "Interactive cryptography demonstration with Alice and Bob.",
            hack_title: "Hacker Console",
            hack_desc: "Hacker Console triggers a phishing message. One wrong click can lead to account takeover.",
            hacked_final_title: "SECURITY ALERT",
            hacked_final_desc: "System compromised via password vulnerability. Be careful with Phishing attacks!",
            exit_btn: "EXIT TOUR"
        }
    };
    /* ================================================================
    THE DIRECTOR'S CUT — CINEMA DIRECTOR CLASS
    ================================================================ */
    class CinemaDirector {
        constructor() {
            this.driver = null;
            this.isVN = currentLang === 'vi';
            this.t = tourConfig[this.isVN ? 'vi' : 'en'];
            this.backdrop = document.getElementById('cinematicBackdrop');
            this.cursor = document.getElementById('fakeCursor');
            this.exitBtn = document.getElementById('exitTourBtn');
        }

        async wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

        async showBackdrop(show = true) {
            if (this.backdrop) {
                if (show) {
                    this.backdrop.classList.add('show');
                    this.exitBtn.style.display = 'block';
                    this.exitBtn.innerText = this.t.exit_btn;
                } else {
                    this.backdrop.classList.remove('show');
                    this.exitBtn.style.display = 'none';
                }
            }
            await this.wait(500);
        }

        async moveCursor(elementSelector) {
            const el = document.querySelector(elementSelector);
            if (!el || !this.cursor) return;
            const rect = el.getBoundingClientRect();
            this.cursor.style.display = 'block';
            this.cursor.style.left = `${rect.left + rect.width/2}px`;
            this.cursor.style.top = `${rect.top + rect.height/2}px`;
            await this.wait(1000);
        }

        async typeText(elementId, text) {
            const el = document.getElementById(elementId);
            if (!el) return;
            el.value = "";
            for (const char of text) {
                el.value += char;
                el.dispatchEvent(new Event('input'));
                await this.wait(30 + Math.random() * 50);
            }
        }

        async showMatrixTerminal() {
            const terminal = document.getElementById('matrixTerminal');
            const content = document.getElementById('matrixContent');
            if (!terminal || !content) return;
            
            terminal.classList.add('show');
            const lines = [
                t('hackerBreach'),
                t('hackerSource'),
                t('hackerWarn'),
                t('hackerAccess'),
                t('hackerRotate'),
                t('hackerExfil'),
                t('hackerCompromised'),
                "------------------------------------",
                t('hackerTakeover')
            ];
            
            for (const line of lines) {
                const p = document.createElement('div');
                p.className = 'matrix-line';
                p.textContent = line;
                content.appendChild(p);
                await this.wait(400);
            }
            await this.wait(1500);
            terminal.classList.remove('show');
            content.innerHTML = "";
        }

        initDriver(steps) {
            this.driver = window.driver.js.driver({
                showProgress: true,
                allowClose: true,
                overlayColor: 'rgba(0, 0, 0, 0.85)',
                popoverClass: 'driverjs-theme',
                nextBtnText: this.isVN ? 'Tiếp theo' : 'Next',
                prevBtnText: this.isVN ? 'Trước đó' : 'Prev',
                doneBtnText: this.isVN ? 'Xong' : 'Done',
                onCloseClick: () => {
                    this.showBackdrop(false);
                },
                steps: steps
            });
        }

        async startStage1() {
            const session = getAliceSession();
            if (!session.loggedIn) {
                showToast(this.isVN ? "Vui lòng đăng nhập trước khi bắt đầu tour!" : "Please login before starting the tour!");
                openAuthModal();
                return;
            }

            // Start on Project Page as required
            switchPage('project');
            await this.wait(500);

            await this.showBackdrop(true);

            // Check if user has already completed the tour
            if (localStorage.getItem('secureMessengerTourCompleted')) {
                showToast(this.isVN ? "Bạn đã hoàn thành hướng dẫn rồi!" : "You've already completed the tour!", 3000);
                return;
            }

            const steps = [
                // Bước 1: Thiết lập cá nhân (Ngôn ngữ & Giao diện)
                {
                    element: '.utility-dock',
                    popover: {
                        title: this.t.setup_title,
                        description: this.t.setup_desc,
                        side: "bottom"
                    }
                },
                // Bước 2: Khám phá thông tin hệ thống (Dự án)
                {
                    element: '#btn-project',
                    popover: {
                        title: this.t.project_title,
                        description: this.t.project_desc,
                        side: "bottom",
                        onNextClick: async () => {
                            switchPage('project');
                            await this.wait(600);
                            this.driver.moveNext();
                        }
                    }
                },
                // Bước 3: Gặp gỡ đội ngũ (Đội ngũ)
                {
                    element: '#btn-team',
                    popover: {
                        title: this.t.team_title,
                        description: this.t.team_desc,
                        side: "bottom",
                        onNextClick: async () => {
                            switchPage('team');
                            await this.wait(600);
                            this.driver.moveNext();
                        }
                    }
                },
                // Bước 4: Quản lý kết nối (Bạn bè)
                {
                    element: '.app-nav a[data-page="friends"]',
                    popover: {
                        title: this.t.friends_title,
                        description: this.t.friends_desc,
                        side: "bottom",
                        onNextClick: async () => {
                            switchPage('friends');
                            await this.wait(600);
                            this.driver.moveNext();
                        }
                    }
                },
                // Bước 5: Trải nghiệm nhắn tin (Trang chủ)
                {
                    element: '.app-nav a[data-page="home"]',
                    popover: {
                        title: this.t.chat_title,
                        description: this.t.chat_desc,
                        side: "bottom",
                        onNextClick: async () => {
                            switchPage('home');
                            await this.wait(600);
                            // Auto-focus vào ô input tin nhắn
                            const messageInput = document.querySelector('.message-input');
                            if (messageInput) {
                                messageInput.focus();
                                messageInput.placeholder = this.isVN ? "Thử gửi 'Xin chào'..." : "Try sending 'Hello'...";
                            }
                            this.driver.moveNext();
                        }
                    }
                }
            ];

            this.initDriver(steps);
            this.driver.drive();

            const _origDestroy = this.driver.destroy;
            const self = this;
            this.driver.destroy = function() {
                _origDestroy.call(self.driver);
                // Mark tour as completed in localStorage
                localStorage.setItem('secureMessengerTourCompleted', 'true');
                // logic to show confirm box
                self.showConfirmation();
            };
        }

        async renderHome() {
            // Internal function to trigger app's home rendering
            if (window.switchPage) {
                window.switchPage('home');
            } else {
                // Fallback to location hash if function not found
                window.location.hash = "#home";
            }
            await this.wait(800); // Wait for page to load as suggested
        }

        showConfirmation() {
            const overlay = document.getElementById('tourConfirmOverlay');
            const title = document.getElementById('confirmTitle');
            const desc = document.getElementById('confirmDesc');
            const yesBtn = document.getElementById('confirmYes');
            const noBtn = document.getElementById('confirmNo');

            title.innerText = this.t.confirm_title;
            desc.innerText = this.t.confirm_desc;
            yesBtn.innerText = this.t.confirm_yes;
            noBtn.innerText = this.t.confirm_no;

            overlay.classList.add('show');

            yesBtn.onclick = async () => {
                overlay.classList.remove('show');
                await this.renderHome();
                this.startStage2();
            };
            noBtn.onclick = () => {
                overlay.classList.remove('show');
                this.showBackdrop(false);
            };
        }

        async startStage2() {
            await this.showBackdrop(true);
            // Already switched to home in confirm box handler
            await this.wait(200);

            // 1. Demo Chat
            this.initDriver([{
                element: '.alice',
                popover: {
                    title: this.t.alice_typing_title,
                    description: this.t.alice_typing_desc,
                    side: "right"
                }
            }]);
            this.driver.drive();
            await this.typeText('aliceInput', this.isVN ? "Chào Bob, đây là tin nhắn mã hóa!" : "Hi Bob, this is an encrypted message!");
            await this.wait(1500);

            // 2. Blackbox Logic - Highlighting Ratchet Monitor
            this.driver.destroy();
            this.initDriver([{
                element: '.column.process',
                popover: {
                    title: this.t.blackbox_title,
                    description: this.t.blackbox_desc,
                    side: "left"
                }
            }]);
            this.driver.drive();
            
            // Trigger send
            sendData('Alice');
            
            const logEntries = document.querySelectorAll('#processLog .log-entry');
            if (logEntries.length > 0) {
                const values = logEntries[0].querySelectorAll('.log-value, .key-chip');
                values.forEach(v => v.classList.add('animating-number'));
                for (let i = 0; i < 20; i++) { // More jumps for better effect
                    values.forEach(v => {
                        if (v.textContent.length > 8) v.textContent = CryptoJS.lib.WordArray.random(12).toString();
                    });
                    await this.wait(100); // Faster jumps
                }
                values.forEach(v => v.classList.remove('animating-number'));
            }
            await this.wait(2000);

            // 3. Demo Ảnh - Pixel Blur
            this.driver.destroy();
            this.initDriver([{
                element: '.column.bob .message-area',
                popover: {
                    title: this.t.pixel_title,
                    description: this.t.pixel_desc,
                    side: "left"
                }
            }]);
            this.driver.drive();

            const bobOutput = document.getElementById('bobOutput');
            const imgDiv = document.createElement('div');
            imgDiv.className = 'bubble friend';
            const imgEl = document.createElement('img');
            imgEl.src = "https://i.pinimg.com/474x/da/0f/a7/da0fa7de15df525903d9d306bc229b09.jpg";
            imgEl.className = "bubble-img pixel-blur";
            imgDiv.appendChild(imgEl);
            bobOutput.appendChild(imgDiv);
            bobOutput.scrollTop = bobOutput.scrollHeight;

            await this.wait(2500);
            imgEl.classList.add('clear');
            await this.wait(2000);

            // 4. Demo Hack - Matrix Scenario
            this.driver.destroy();
            this.initDriver([{
                element: '.xss-btn',
                popover: {
                    title: this.t.hack_title,
                    description: this.t.hack_desc,
                    side: "bottom"
                }
            }]);
            this.driver.drive();
            await this.wait(2000);

            triggerXSSAttack();
            await this.wait(2000);

            this.driver.destroy();
            await this.moveCursor('#aliceOutput .bubble.friend b');
            showFakePasswordPrompt();
            await this.wait(1500);

            // Matrix Terminal Effect - NO JUMPSCARE
            await this.showMatrixTerminal();

            // Final Breach
            document.body.classList.add('red-alert-bg');
            document.querySelector('.layout').classList.add('glitch-active');
            
            const pwdInput = document.getElementById('xssPassword');
            if (pwdInput) {
                for (const char of "secret123") {
                    pwdInput.value += char;
                    await this.wait(100);
                }
            }
            await this.wait(1000);
            
            executeAccountTakeover();
            
            const alertMsg = document.createElement('div');
            alertMsg.className = 'hacked-overlay-msg';
            alertMsg.innerHTML = `
                <div class="tour-confirm-card" style="border-color:#ff4757; background:rgba(10,0,0,0.95); z-index: 2000001;">
                    <h1 style="color:#ff4757; font-family:'JetBrains Mono';">🚨 SECURITY ALERT</h1>
                    <p style="color:#fff;">${this.t.hacked_final_desc}</p>
                    <button onclick="location.reload()" class="tour-btn tour-btn-yes">RESTART SYSTEM</button>
                </div>
            `;
            document.body.appendChild(alertMsg);
            
            await this.wait(4000);
            document.querySelector('.layout').classList.remove('glitch-active');
        }
    }

    window.startMyTour = function(e) {
        if (e) e.preventDefault();
        
        console.log('Starting interactive tour...');
        
        // Clean up previous tour instance if exists
        if (window.tourActive) {
            return;
        }
        window.tourActive = true;
        
        // Reset any lingering listeners from previous tour
        const sendBtn = document.querySelector('.column.alice .send-btn');
        if (sendBtn && sendBtn.getAttribute('data-tour-original')) {
            const original = sendBtn.getAttribute('data-tour-original');
            sendBtn.onclick = new Function(original);
            sendBtn.removeAttribute('data-tour-original');
        }
        
        // Get current language for bilingual support
        const isVN = currentLang === 'vi';
        
        // Check if user is logged in
        const session = getAliceSession();
        const isLoggedIn = session.loggedIn;
        
        // Define steps for first-time visitors (includes login steps)
        const firstTimeSteps = [
                // BƯỚC 1: Hướng dẫn nhấn nút đăng nhập
                {
                    element: '#authToggleBtn',
                    popover: {
                        title: isVN ? 'BƯỚC 1: ĐĂNG NHẬP HỆ THỐNG' : "STEP 1: SYSTEM LOGIN",
                        description: isVN ? 'Nhấn vào nút đăng nhập để bắt đầu trải nghiệm Secure Messenger!' : 'Click the login button to start your Secure Messenger experience!',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        // Kiểm tra xem đã đăng nhập chưa
                        const session = getAliceSession();
                        if (session.loggedIn) {
                            showToast(isVN ? 'Bạn đã đăng nhập rồi! Chuyển sang bước tiếp theo...' : 'You are already logged in! Moving to next step...', 2000);
                            setTimeout(() => driverObj.moveNext(), 1500);
                        } else {
                            setTimeout(() => {
                                element.click();
                                showToast(isVN ? 'Đã mở form đăng nhập!' : 'Login form opened!', 2000);
                                setTimeout(() => driverObj.moveNext(), 1500);
                            }, 2000);
                        }
                    }
                },
                
                // BƯỚC 2: Tô sáng form đăng nhập
                {
                    element: '.auth-card',
                    popover: {
                        title: isVN ? 'BƯỚC 2: FORM ĐĂNG NHẬP' : 'STEP 2: LOGIN FORM',
                        description: isVN ? 'Đây là form đăng nhập. Chúng ta sẽ điền thông tin tài khoản Alice.' : 'This is the login form. We will fill in Alice account information.',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            showToast(isVN ? 'Sẵn sàng điền thông tin đăng nhập!' : 'Ready to fill in login information!', 2000);
                            setTimeout(() => driverObj.moveNext(), 2000);
                        }, 1000);
                    }
                },
                
                // BƯỚC 3: Hướng dẫn nhập tên
                {
                    element: '#authName',
                    popover: {
                        title: isVN ? 'BƯỚC 3: NHẬP TÊN TÀI KHOẢN' : 'STEP 3: ENTER ACCOUNT NAME',
                        description: isVN ? 'Nhập tên "Alice" vào ô này. Hệ thống sẽ tự động chuyển bước khi bạn nhập xong.' : 'Enter "Alice" in this field. The system will automatically move to next step when you finish typing.',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.focus();
                            element.value = '';
                            showToast(isVN ? 'Vui lòng nhập "Alice"' : 'Please enter "Alice"', 3000);
                            
                            // Chờ người dùng nhập xong rồi mới chuyển bước
                            const waitForInput = setInterval(() => {
                                if (element.value.trim().toLowerCase() === 'alice') {
                                    clearInterval(waitForInput);
                                    showToast(isVN ? 'Đúng rồi! Chuyển sang bước tiếp theo...' : 'Correct! Moving to next step...', 1500);
                                    setTimeout(() => driverObj.moveNext(), 1500);
                                }
                            }, 500);
                        }, 1000);
                    }
                },
                
                // BƯỚC 4: Hướng dẫn nhập email
                {
                    element: '#authEmail',
                    popover: {
                        title: isVN ? 'BƯỚC 4: NHẬP EMAIL' : 'STEP 4: ENTER EMAIL',
                        description: isVN ? 'Nhập email "alice@example.com". Hệ thống sẽ tự động chuyển bước khi bạn nhập xong.' : 'Enter "alice@example.com". The system will automatically move to next step when you finish typing.',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.focus();
                            element.value = '';
                            showToast(isVN ? 'Vui lòng nhập "alice@example.com"' : 'Please enter "alice@example.com"', 3000);
                            
                            // Chờ người dùng nhập xong rồi mới chuyển bước
                            const waitForInput = setInterval(() => {
                                if (element.value.trim().toLowerCase() === 'alice@example.com') {
                                    clearInterval(waitForInput);
                                    showToast(isVN ? 'Hoàn thành! Chuyển sang bước cuối...' : 'Complete! Moving to final step...', 1500);
                                    setTimeout(() => driverObj.moveNext(), 1500);
                                }
                            }, 500);
                        }, 1000);
                    }
                },
                
                // BƯỚC 5: Hướng dẫn nhấn nút đăng nhập
                {
                    element: '#loginSubmitBtn',
                    popover: {
                        title: isVN ? 'BƯỚC 5: HOÀN TẤT ĐĂNG NHẬP' : 'STEP 5: COMPLETE LOGIN',
                        description: isVN ? 'Nhấn nút "Đăng nhập" để hoàn tất và tiếp tục tour!' : 'Click the "Login" button to complete and continue the tour!',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        // Đảm bảo modal đã sẵn sàng và nút có thể được tìm thấy
                        setTimeout(() => {
                            // Kiểm tra lại nút đăng nhập
                            const loginBtn = document.getElementById('loginSubmitBtn');
                            if (loginBtn) {
                                loginBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                showToast(isVN ? 'Nhấn nút đăng nhập để hoàn tất!' : 'Click login button to complete!', 3000);
                                
                                // Lắng nghe sự kiện click vào nút đăng nhập
                                const handleLoginClick = function(e) {
                                    e.preventDefault();
                                    loginBtn.removeEventListener('click', handleLoginClick);
                                    showToast(isVN ? 'Đang xử lý đăng nhập...' : 'Processing login...', 2000);
                                    
                                    // Gọi hàm đăng nhập
                                    submitAliceLogin();
                                    
                                    // Lắng nghe sự kiện đóng modal đăng nhập
                                    const checkLogin = setInterval(() => {
                                        const authModal = document.getElementById('authModal');
                                        const session = getAliceSession();
                                        
                                        if (!authModal.classList.contains('show') && session.loggedIn) {
                                            clearInterval(checkLogin);
                                            showToast(isVN ? 'Đăng nhập thành công! Tiếp tục tour...' : 'Login successful! Continuing tour...', 2000);
                                            setTimeout(() => driverObj.moveNext(), 2000);
                                        }
                                    }, 500);
                                };
                                
                                loginBtn.addEventListener('click', handleLoginClick);
                            } else {
                                console.error('Login button not found!');
                                showToast(isVN ? 'Không tìm thấy nút đăng nhập!' : 'Login button not found!', 2000);
                                setTimeout(() => driverObj.moveNext(), 2000);
                            }
                        }, 1500);
                    }
                },
                {
                    element: '.utility-dock-icon:first-child',
                    popover: {
                        title: isVN ? 'NGÔN NGỮ' : "LANGUAGE",
                        description: isVN ? 'Lựa chọn ngôn ngữ phù hợp với bạn' : 'Select your preferred language.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.click();
                            showToast(isVN ? 'Đã chuyển ngôn ngữ!' : 'Language switched!', 2000);
                            // Đợi một chút để UI cập nhật rồi mới chuyển bước
                            setTimeout(() => {
                                // Refresh lại highlight để tránh bị lệch
                                driverObj.refresh();
                                setTimeout(() => driverObj.moveNext(), 1000);
                            }, 1000);
                        }, 2000);
                    }
                },
                {
                    element: '.utility-dock-icon:last-child',
                    popover: {
                        title: isVN ? 'CHẾ ĐỘ SÁNG/TỐI' : 'LIGHT/DARK MODE',
                        description: isVN ? 'Chế độ sáng/tối sẽ thay đổi giao diện phù hợp với môi trường của bạn.' : 'The app will change interface to suit your environment.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.click();
                            showToast(isVN ? 'Đã chuyển chế độ!' : 'Mode changed!', 2000);
                            // Đợi một chút để UI cập nhật rồi mới chuyển bước
                            setTimeout(() => {
                                // Refresh lại highlight để tránh bị lệch
                                driverObj.refresh();
                                setTimeout(() => driverObj.moveNext(), 1000);
                            }, 1000);
                        }, 2000);
                    }
                },
                {
                    element: '#btn-project',
                    popover: {
                        title: isVN ? 'TRANG DỰ ÁN' : 'PROJECT PAGE',
                        description: isVN ? 'Hệ thống đang mở trang thông tin dự án và lý thuyết mã hóa...' : 'Opening project information and encryption theory...',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('project');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã mở trang Dự án!' : 'Opened Project page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 1800);
                        }, 3000);
                    }
                },
                {
                    element: '#btn-team',
                    popover: {
                        title: isVN ? 'TRANG ĐỘI NGŨ' : 'TEAM PAGE',
                        description: isVN ? 'Đây là nơi giới thiệu các thành viên đã phát triển sản phẩm.' : 'This is where we introduce the members who developed the product.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('team');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã mở trang Đội ngũ!' : 'Opened Team page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 1800);
                        }, 3000);
                    }
                },
                {
                    element: '.app-nav a[data-page="home"]',
                    popover: {
                        title: isVN ? 'BƯỚC 10: TRANG CHỦ' : 'STEP 10: HOME PAGE',
                        description: isVN ? 'Nhấn vào nút trang chủ để quay lại nơi gửi tin nhắn được mã hóa E2E.' : 'Click home button to return to the E2E encrypted messaging page.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('home');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã quay lại Trang chủ!' : 'Returned to Home page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 2000);
                        }, 1000);
                    }
                },
                // BƯỚC 11: Nhập tin nhắn "Chào thế giới"
                {
                    element: '#aliceInput',
                    popover: {
                        title: isVN ? 'BƯỚC 11: NHẬP TIN NHẮN' : 'STEP 11: MESSAGE INPUT',
                        description: isVN ? 'Nhập chính xác "Chào thế giới". Hệ thống sẽ tự động chuyển bước khi bạn nhập đúng.' : 'Type exactly "Hello World". The system will automatically move to next step when you type correctly.',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.focus();
                            element.value = '';
                            element.placeholder = isVN ? "Nhập 'Chào thế giới'..." : "Type 'Hello World'...";
                            showToast(isVN ? 'Vui lòng nhập "Chào thế giới"' : 'Please type "Hello World"', 3000);
                            
                            // Chờ người dùng nhập đúng rồi mới chuyển bước
                            const waitForInput = setInterval(() => {
                                if (element.value.trim() === (isVN ? 'Chào thế giới' : 'Hello World')) {
                                    clearInterval(waitForInput);
                                    showToast(isVN ? 'Đúng rồi! Chuyển sang bước tiếp theo...' : 'Correct! Moving to next step...', 1500);
                                    setTimeout(() => driverObj.moveNext(), 1500);
                                }
                            }, 500);
                        }, 1000);
                    }
                },
                // BƯỚC 12: Gửi tin nhắn
                {
                    element: '.column.alice .send-btn',
                    popover: {
                        title: isVN ? 'BƯỚC 12: GỬI TIN NHẮN' : 'STEP 12: SEND MESSAGE',
                        description: isVN ? 'Nhấn nút gửi để hoàn tất. Tin nhắn sẽ được mã hóa E2E ngay lập tức!' : 'Press the send button to complete. Your message will be E2E encrypted instantly!',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        const sendBtn = document.querySelector('.column.alice .send-btn');
                        if (sendBtn) {
                            const originalOnClick = sendBtn.getAttribute('onclick');
                            sendBtn.setAttribute('data-tour-original', originalOnClick);
                            sendBtn.onclick = function(e) {
                                const msgInput = document.getElementById('aliceInput');
                                if (msgInput && msgInput.value.trim() === (isVN ? 'Chào thế giới' : 'Hello World')) {
                                    // Gọi hàm sendData an toàn thay vì eval()
                                    window.sendData('Alice');
                                    showToast(isVN ? 'Tin nhắn đã được gửi! Chuyển sang bước tiếp theo...' : 'Message sent! Moving to next step...', 2000);
                                    setTimeout(() => driverObj.moveNext(), 2000);
                                } else {
                                    showToast(isVN ? 'Vui lòng nhập đúng "Chào thế giới"!' : 'Please type exactly "Hello World"!', 2000);
                                }
                            };
                        }
                        showToast(isVN ? 'Hãy gửi tin nhắn "Chào thế giới"!' : 'Please send message "Hello World"!', 3000);
                    }
                },
                // BƯỚC 14: KẾT THÚC TUTORIAL
                {
                    element: '.layout',
                    popover: {
                        title: isVN ? '🎉 TUTORIAL HOÀN TẤT!' : '🎉 TUTORIAL COMPLETED!',
                        description: isVN ? 'Bạn đã hoàn thành toàn bộ tutorial! Bạn đã học được:' + '\n\n' +
                                    '✅ Cách gửi tin nhắn an toàn' + '\n' +
                                    '✅ Hiểu về mã hóa end-to-end' + '\n' +
                                    '✅ Nhận diện tấn công Eve Hack' + '\n' +
                                    '✅ Cách bảo vệ tài khoản' + '\n\n' +
                                    'Cảm ơn bạn đã trải nghiệm!' : 
                                    'You have completed the entire tutorial! You have learned:' + '\n\n' +
                                    '✅ How to send secure messages' + '\n' +
                                    '✅ Understanding end-to-end encryption' + '\n' +
                                    '✅ Recognizing Eve Hack attacks' + '\n' +
                                    '✅ How to protect your account' + '\n\n' +
                                    'Thank you for the experience!',
                        side: 'center',
                        align: 'center'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            localStorage.setItem('secureMessengerTourCompleted', 'true');
                            window.tourActive = false;
                            showToast(isVN ? 'Tutorial hoàn tất! Cảm ơn bạn!' : 'Tutorial completed! Thank you!', 5000);
                        }, 2000);
                    }
                }
            ];
        
        // Define steps for logged-in users (starts from language step)
        const loggedInSteps = [
                {
                    element: '.utility-dock-icon:first-child',
                    popover: {
                        title: isVN ? 'NGÔN NGỮ' : "LANGUAGE",
                        description: isVN ? 'Lựa chọn ngôn ngữ phù hợp với bạn' : 'Select your preferred language.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.click();
                            showToast(isVN ? 'Đã chuyển ngôn ngữ!' : 'Language switched!', 2000);
                            // Đợi một chút để UI cập nhật rồi mới chuyển bước
                            setTimeout(() => {
                                // Refresh lại highlight để tránh bị lệch
                                driverObj.refresh();
                                setTimeout(() => driverObj.moveNext(), 1000);
                            }, 1000);
                        }, 2000);
                    }
                },
                {
                    element: '.utility-dock-icon:last-child',
                    popover: {
                        title: isVN ? 'CHẾ ĐỘ SÁNG/TỐI' : 'LIGHT/DARK MODE',
                        description: isVN ? 'Chế độ sáng/tối sẽ thay đổi giao diện phù hợp với môi trường của bạn.' : 'The app will change interface to suit your environment.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.click();
                            showToast(isVN ? 'Đã chuyển chế độ!' : 'Mode changed!', 2000);
                            // Đợi một chút để UI cập nhật rồi mới chuyển bước
                            setTimeout(() => {
                                // Refresh lại highlight để tránh bị lệch
                                driverObj.refresh();
                                setTimeout(() => driverObj.moveNext(), 1000);
                            }, 1000);
                        }, 2000);
                    }
                },
                {
                    element: '#btn-project',
                    popover: {
                        title: isVN ? 'TRANG DỰ ÁN' : 'PROJECT PAGE',
                        description: isVN ? 'Hệ thống đang mở trang thông tin dự án và lý thuyết mã hóa...' : 'Opening project information and encryption theory...',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('project');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã mở trang Dự án!' : 'Opened Project page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 1800);
                        }, 3000);
                    }
                },
                {
                    element: '#btn-team',
                    popover: {
                        title: isVN ? 'TRANG ĐỘI NGŨ' : 'TEAM PAGE',
                        description: isVN ? 'Đây là nơi giới thiệu các thành viên đã phát triển sản phẩm.' : 'This is where we introduce the members who developed the product.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('team');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã mở trang Đội ngũ!' : 'Opened Team page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 1800);
                        }, 3000);
                    }
                },
                {
                    element: '.app-nav a[data-page="home"]',
                    popover: {
                        title: isVN ? 'BƯỚC 6: TRANG CHỦ' : 'STEP 6: HOME PAGE',
                        description: isVN ? 'Nhấn vào nút trang chủ để quay lại nơi gửi tin nhắn được mã hóa E2E.' : 'Click home button to return to the E2E encrypted messaging page.',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            if (window.switchPage) {
                                window.switchPage('home');
                            } else {
                                element.click();
                            }
                            showToast(isVN ? 'Đã quay lại Trang chủ!' : 'Returned to Home page!', 2000);
                            setTimeout(() => driverObj.moveNext(), 2000);
                        }, 1000);
                    }
                },
                // BƯỚC 7: Nhập tin nhắn "Chào thế giới"
                {
                    element: '#aliceInput',
                    popover: {
                        title: isVN ? 'BƯỚC 7: NHẬP TIN NHẮN' : 'STEP 7: MESSAGE INPUT',
                        description: isVN ? 'Nhập chính xác "Chào thế giới". Hệ thống sẽ tự động chuyển bước khi bạn nhập đúng.' : 'Type exactly "Hello World". The system will automatically move to next step when you type correctly.',
                        side: 'top'
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            element.focus();
                            element.value = '';
                            element.placeholder = isVN ? "Nhập 'Chào thế giới'..." : "Type 'Hello World'...";
                            showToast(isVN ? 'Vui lòng nhập "Chào thế giới"' : 'Please type "Hello World"', 3000);
                            
                            // Chờ người dùng nhập đúng rồi mới chuyển bước
                            const waitForInput = setInterval(() => {
                                if (element.value.trim() === (isVN ? 'Chào thế giới' : 'Hello World')) {
                                    clearInterval(waitForInput);
                                    showToast(isVN ? 'Đúng rồi! Chuyển sang bước tiếp theo...' : 'Correct! Moving to next step...', 1500);
                                    setTimeout(() => driverObj.moveNext(), 1500);
                                }
                            }, 500);
                        }, 1000);
                    }
                },
                // BƯỚC 8: Gửi tin nhắn
                {
                    element: '.column.alice .send-btn',
                    popover: {
                        title: isVN ? 'BƯỚC 8: GỬI TIN NHẮN' : 'STEP 8: SEND MESSAGE',
                        description: isVN ? 'Nhấn nút gửi để hoàn tất. Tin nhắn sẽ được mã hóa E2E ngay lập tức!' : 'Press the send button to complete. Your message will be E2E encrypted instantly!',
                        side: 'bottom'
                    },
                    onHighlightStarted: (element) => {
                        const sendBtn = document.querySelector('.column.alice .send-btn');
                        if (sendBtn) {
                            const originalOnClick = sendBtn.getAttribute('onclick');
                            sendBtn.setAttribute('data-tour-original', originalOnClick);
                            sendBtn.onclick = function(e) {
                                const msgInput = document.getElementById('aliceInput');
                                if (msgInput && msgInput.value.trim() === (isVN ? 'Chào thế giới' : 'Hello World')) {
                                    // Gọi hàm sendData an toàn thay vì eval()
                                    window.sendData('Alice');
                                    showToast(isVN ? 'Tin nhắn đã được gửi! Chuyển sang bước tiếp theo...' : 'Message sent! Moving to next step...', 2000);
                                    setTimeout(() => driverObj.moveNext(), 2000);
                                } else {
                                    showToast(isVN ? 'Vui lòng nhập đúng "Chào thế giới"!' : 'Please type exactly "Hello World"!', 2000);
                                }
                            };
                        }
                        showToast(isVN ? 'Hãy gửi tin nhắn "Chào thế giới"!' : 'Please send message "Hello World"!', 3000);
                    }
                },
                // BƯỚC 9: KẾT THÚC TUTORIAL
                {
                    element: '.layout',
                    popover: {
                        title: isVN ? '🎉 TUTORIAL HOÀN TẤT!' : '🎉 TUTORIAL COMPLETED!',
                        description: isVN ? 'Bạn đã hoàn thành toàn bộ tutorial! Bạn đã học được:' + '\n\n' +
                                    '✅ Cách gửi tin nhắn an toàn' + '\n' +
                                    '✅ Hiểu về mã hóa end-to-end' + '\n' +
                                    '✅ Nhận diện tấn công Eve Hack' + '\n' +
                                    '✅ Cách bảo vệ tài khoản' + '\n\n' +
                                    'Cảm ơn bạn đã trải nghiệm!' : 
                                    'You have completed the entire tutorial! You have learned:' + '\n\n' +
                                    '✅ How to send secure messages' + '\n' +
                                    '✅ Understanding end-to-end encryption' + '\n' +
                                    '✅ Recognizing Eve Hack attacks' + '\n' +
                                    '✅ How to protect your account' + '\n\n' +
                                    'Thank you for the experience!',
                        showButtons: false,
                    },
                    onHighlightStarted: (element) => {
                        setTimeout(() => {
                            localStorage.setItem('secureMessengerTourCompleted', 'true');
                            window.tourActive = false;
                            showToast(isVN ? 'Tutorial hoàn tất! Cảm ơn bạn!' : 'Tutorial completed! Thank you!', 5000);
                        }, 2000);
                    }
                }
            ];
        
        // Interactive tour with automatic actions
        const driverObj = window.driver.js.driver({
            showProgress: true,
            allowClose: true,
            animate: false,
            overlayColor: 'rgba(0, 0, 0, 0.85)',
            nextBtnText: isVN ? 'Tiếp theo' : 'Next',
            prevBtnText: isVN ? 'Trước đó' : 'Prev',
            doneBtnText: isVN ? 'Hoàn thành' : 'Done',
            onCloseClick: () => {
                window.tourActive = false;
            },
            steps: isLoggedIn ? loggedInSteps : firstTimeSteps
        });
        
        driverObj.drive();
    };

    window.resetTour = function() {
        localStorage.removeItem('secureMessengerTourCompleted');
        showToast('Tour reset! You can start the tour again.', 3000);
    };

    
    
    const tourBtn = document.getElementById('start-tour');
    if (tourBtn) {
        tourBtn.onclick = (e) => window.startMyTour(e);
    };