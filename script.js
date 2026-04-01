// 古风码字页面JavaScript功能

class AncientWritingApp {
    constructor() {
        this.editor = document.getElementById('editor');
        this.charCount = document.getElementById('charCount');
        this.clearBtn = document.getElementById('clearBtn');
        this.clearModeBtn = document.getElementById('clearModeBtn');
        this.saveBtn = document.getElementById('saveBtn');
        this.exportBtn = document.getElementById('exportBtn');
        this.fontBtn = document.getElementById('fontBtn');
        this.themeBtn = document.getElementById('themeBtn');
        this.musicBtn = document.getElementById('musicBtn');
        this.switchMusicBtn = document.getElementById('switchMusicBtn');
        this.bgMusic = document.getElementById('bgMusic');
        this.musicWave = document.getElementById('musicWave');
        this.quoteText = document.getElementById('quoteText');
        this.floatingQuote = document.getElementById('floatingQuote');
        this.fadingContainer = document.getElementById('fadingContainer');
        this.rainContainer = document.getElementById('rainContainer');
        
        this.quotes = [
            '笔落惊风雨，诗成泣鬼神',
            '读书破万卷，下笔如有神',
            '文章本天成，妙手偶得之',
            '清水出芙蓉，天然去雕饰',
            '吟安一个字，捻断数茎须',
            '为人性僻耽佳句，语不惊人死不休',
            '两句三年得，一吟双泪流',
            '文章千古事，得失寸心知',
            '读书不觉春已深，一寸光阴一寸金',
            '书山有路勤为径，学海无涯苦作舟'
        ];
        
        this.fonts = [
            "'楷体', 'KaiTi', 'Microsoft YaHei', sans-serif",
            "'宋体', 'SimSun', 'serif'",
            "'黑体', 'SimHei', 'sans-serif'",
            "'隶书', 'LiSu', 'cursive'"
        ];
        
        this.currentFontIndex = 0;
        this.isDarkTheme = false;
        this.isPlaying = false;
        this.deletingText = false;
        this.clearWithConfirm = true;
        
        this.musicList = [
            { name: '可惜没有如果', file: 'music/可惜没有如果.mp3' },
            { name: '平凡之路', file: 'music/平凡之路.mp3' }
        ];
        this.currentMusicIndex = 0;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateCharCount();
        this.showRandomQuote();
        this.initRainEffect();
        this.updateClearModeDisplay();
        setInterval(() => this.showRandomQuote(), 15000); // 每15秒换一句
    }
    
    bindEvents() {
        // 清空按钮
        this.clearBtn.addEventListener('click', () => this.clearContent());
        
        // 清空模式按钮
        this.clearModeBtn.addEventListener('click', () => this.toggleClearMode());
        
        // 保存按钮
        this.saveBtn.addEventListener('click', () => this.saveContent());
        
        // 导出按钮
        this.exportBtn.addEventListener('click', () => this.exportContent());
        
        // 字体按钮
        this.fontBtn.addEventListener('click', () => this.changeFont());
        
        // 主题按钮
        this.themeBtn.addEventListener('click', () => this.toggleTheme());
        
        // 音乐按钮
        this.musicBtn.addEventListener('click', () => this.toggleMusic());
        
        // 音乐切换按钮
        this.switchMusicBtn.addEventListener('click', () => this.switchMusic());
        
        // 编辑器事件
        this.editor.addEventListener('input', () => this.handleEditorInput());
        this.editor.addEventListener('paste', (e) => this.handlePaste(e));
        this.editor.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // 点击空白处隐藏浮动的诗句
        document.addEventListener('click', (e) => {
            if (!this.floatingQuote.contains(e.target)) {
                this.floatingQuote.classList.remove('show');
            }
        });
    }
    
    updateCharCount() {
        const text = this.editor.textContent || '';
        const charCount = text.replace(/\s/g, '').length;
        this.charCount.textContent = charCount;
    }
    
    clearContent() {
        if (this.clearWithConfirm) {
            if (confirm('确定要清空笔墨吗？此操作不可撤销。')) {
                this.clearContentWithoutConfirm();
            }
        } else {
            this.clearContentWithoutConfirm();
        }
    }
    
    clearContentWithoutConfirm() {
        // 创建清空动效
        this.createClearEffect();
        
        setTimeout(() => {
            this.editor.innerHTML = '';
            this.updateCharCount();
            this.showNotification('笔墨已清空');
        }, 500);
    }
    
    createClearEffect() {
        const paper = document.querySelector('.paper');
        paper.style.transition = 'transform 0.5s ease';
        paper.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            paper.style.transform = 'scale(1)';
            paper.style.transition = '';
        }, 500);
    }
    
    saveContent() {
        const content = this.editor.innerHTML;
        const text = this.editor.textContent || '';
        
        if (text.trim() === '') {
            this.showNotification('文稿为空，无法保存');
            return;
        }
        
        // 创建下载链接
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const now = new Date();
        const filename = `古韵文稿_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}_${now.getHours().toString().padStart(2,'0')}${now.getMinutes().toString().padStart(2,'0')}.txt`;
        
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('文稿已保存');
    }
    
    changeFont() {
        this.currentFontIndex = (this.currentFontIndex + 1) % this.fonts.length;
        this.editor.style.fontFamily = this.fonts[this.currentFontIndex];
        this.showNotification(`字体已切换至 ${this.getFontName()}`);
    }
    
    getFontName() {
        const fontNames = ['楷体', '宋体', '黑体', '隶书'];
        return fontNames[this.currentFontIndex];
    }
    
    toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
        document.body.classList.toggle('dark-theme');
        this.showNotification(this.isDarkTheme ? '已切换至暗色主题' : '已切换至亮色主题');
    }
    
    toggleMusic() {
        if (this.isPlaying) {
            try {
                this.bgMusic.pause();
                this.musicWave.classList.remove('active');
                this.musicBtn.classList.remove('music-playing');
                this.musicBtn.textContent = '🎵';
                this.showNotification('音乐已暂停');
            } catch (error) {
                console.error('音乐暂停失败:', error);
                this.showNotification('音乐暂停失败');
            }
        } else {
            try {
                this.bgMusic.play().then(() => {
                    this.musicWave.classList.add('active');
                    this.musicBtn.classList.add('music-playing');
                    this.musicBtn.textContent = '⏸️';
                    const currentMusic = this.musicList[this.currentMusicIndex];
                    this.showNotification(`正在播放: ${currentMusic.name}`);
                }).catch((error) => {
                    console.error('音乐播放失败:', error);
                    this.showNotification('音乐播放失败，请检查音乐文件');
                });
            } catch (error) {
                console.error('音乐播放错误:', error);
                this.showNotification('音乐播放出错');
            }
        }
        this.isPlaying = !this.isPlaying;
    }
    
    switchMusic() {
        if (this.musicList.length === 0) {
            this.showNotification('没有可用的音乐文件');
            return;
        }
        
        const wasPlaying = this.isPlaying;
        if (wasPlaying) {
            this.bgMusic.pause();
        }
        
        this.currentMusicIndex = (this.currentMusicIndex + 1) % this.musicList.length;
        const nextMusic = this.musicList[this.currentMusicIndex];
        
        this.bgMusic.src = nextMusic.file;
        
        if (wasPlaying) {
            this.bgMusic.play().then(() => {
                this.showNotification(`已切换至: ${nextMusic.name}`);
            }).catch(() => {
                this.showNotification('音乐切换失败');
            });
        } else {
            this.showNotification(`已切换至: ${nextMusic.name}`);
        }
    }
    
    exportContent() {
        const content = this.editor.innerHTML;
        const text = this.editor.textContent || '';
        
        if (text.trim() === '') {
            this.showNotification('文稿为空，无法导出');
            return;
        }
        
        // 先尝试PDF导出
        if (window.jspdf) {
            this.exportAsPDF(text);
        } else {
            // PDF库不可用，降级为TXT导出
            this.exportAsTXT(text);
        }
    }
    
    exportAsPDF(text) {
        try {
            const { jsPDF } = window.jspdf;
            
            if (typeof html2canvas === 'undefined') {
                throw new Error('html2canvas库未加载');
            }
            
            this.showNotification('正在生成PDF...');
            
            const paperElement = document.querySelector('.paper-content');
            
            html2canvas(paperElement, {
                scale: 2,
                useCORS: true,
                logging: false,
                backgroundColor: '#ffffff'
            }).then(canvas => {
                const imgData = canvas.toDataURL('image/png');
                const doc = new jsPDF('p', 'mm', 'a4');
                
                const now = new Date();
                const title = `古韵文稿_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}`;
                
                const imgWidth = 190;
                const pageHeight = 297;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                let heightLeft = imgHeight;
                let position = 10;
                
                doc.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
                heightLeft -= pageHeight;
                
                while (heightLeft >= 0) {
                    position = heightLeft - imgHeight;
                    doc.addPage();
                    doc.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
                    heightLeft -= pageHeight;
                }
                
                const filename = `${title}.pdf`;
                doc.save(filename);
                
                this.showNotification('PDF导出成功');
            }).catch(error => {
                console.error('PDF生成失败:', error);
                this.showNotification('PDF生成失败，正在导出TXT格式...');
                setTimeout(() => this.exportAsTXT(text), 500);
            });
            
        } catch (error) {
            console.error('PDF导出失败:', error);
            this.showNotification('PDF导出失败，正在导出TXT格式...');
            setTimeout(() => this.exportAsTXT(text), 500);
        }
    }
    
    exportAsTXT(text) {
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const now = new Date();
        const filename = `古韵文稿_${now.getFullYear()}${(now.getMonth()+1).toString().padStart(2,'0')}${now.getDate().toString().padStart(2,'0')}.txt`;
        
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('TXT导出成功');
    }
    
    handleEditorInput() {
        if (this.deletingText) {
            return;
        }
        
        this.updateCharCount();
    }
    
    handleKeyDown(e) {
        // 检测删除操作
        if (e.key === 'Backspace' || e.key === 'Delete') {
            this.deletingText = true;
            setTimeout(() => {
                this.createDeletionEffect();
                this.deletingText = false;
            }, 50);
        }
        
        // 特殊快捷键
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 's':
                    e.preventDefault();
                    this.saveContent();
                    break;
                case 'e':
                    e.preventDefault();
                    this.clearContent();
                    break;
                case 'f':
                    e.preventDefault();
                    this.changeFont();
                    break;
                case 't':
                    e.preventDefault();
                    this.toggleTheme();
                    break;
                case 'm':
                    e.preventDefault();
                    this.toggleMusic();
                    break;
                case 'p':
                    e.preventDefault();
                    this.exportContent();
                    break;
            }
        }
        
        // 自动标点符号美化
        if (e.key === '。') {
            setTimeout(() => {
                this.enhancePunctuation();
            }, 100);
        }
    }
    
    createDeletionEffect() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            
            // 创建散去的文字效果
            this.createFadingChar(rect.left, rect.top);
            
            // 创建墨水粒子效果
            this.createInkParticles(rect.left, rect.top);
        }
    }
    
    createFadingChar(x, y) {
        const chars = ['墨', '韵', '书', '香', '文', '章', '诗', '词'];
        const randomChar = chars[Math.floor(Math.random() * chars.length)];
        
        const fadingChar = document.createElement('div');
        fadingChar.className = 'fading-char';
        fadingChar.textContent = randomChar;
        fadingChar.style.left = `${x}px`;
        fadingChar.style.top = `${y}px`;
        
        this.fadingContainer.appendChild(fadingChar);
        
        // 动画结束后移除元素
        setTimeout(() => {
            if (fadingChar.parentNode) {
                fadingChar.parentNode.removeChild(fadingChar);
            }
        }, 1500);
    }
    
    createInkParticles(x, y) {
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.className = 'ink-particle';
            particle.style.left = `${x + Math.random() * 20 - 10}px`;
            particle.style.top = `${y + Math.random() * 20 - 10}px`;
            particle.style.animationDelay = `${Math.random() * 0.5}s`;
            
            this.fadingContainer.appendChild(particle);
            
            // 动画结束后移除粒子
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 2000);
        }
    }
    
    handlePaste(e) {
        e.preventDefault();
        const text = (e.clipboardData || window.clipboardData).getData('text/plain');
        const selection = window.getSelection();
        
        if (selection.rangeCount) {
            const range = selection.getRangeAt(0);
            range.deleteContents();
            
            const span = document.createElement('span');
            span.textContent = text;
            span.style.color = '#8b4513';
            span.style.fontWeight = 'normal';
            
            range.insertNode(span);
            range.setStartAfter(span);
            range.collapse(true);
            selection.removeAllRanges();
            selection.addRange(range);
        }
        
        this.updateCharCount();
    }
    
    handleKeyDown(e) {
        // 检测删除操作
        if (e.key === 'Backspace' || e.key === 'Delete') {
            this.deletingText = true;
            setTimeout(() => {
                this.createDeletionEffect();
                this.deletingText = false;
            }, 50);
        }
        
        // 特殊快捷键
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 's':
                    e.preventDefault();
                    this.saveContent();
                    break;
                case 'e':
                    e.preventDefault();
                    this.clearContent();
                    break;
                case 'f':
                    e.preventDefault();
                    this.changeFont();
                    break;
                case 't':
                    e.preventDefault();
                    this.toggleTheme();
                    break;
                case 'm':
                    e.preventDefault();
                    this.toggleMusic();
                    break;
                case 'p':
                    e.preventDefault();
                    this.exportContent();
                    break;
            }
        }
        
        // 自动标点符号美化
        if (e.key === '。') {
            setTimeout(() => {
                this.enhancePunctuation();
            }, 100);
        }
    }
    
    initRainEffect() {
        // 创建雨滴
        for (let i = 0; i < 50; i++) {
            this.createRaindrop();
        }
    }
    
    createRaindrop() {
        const raindrop = document.createElement('div');
        raindrop.className = 'raindrop';
        raindrop.style.left = Math.random() * 100 + '%';
        raindrop.style.animationDuration = (Math.random() * 2 + 1) + 's';
        raindrop.style.animationDelay = Math.random() * 2 + 's';
        raindrop.style.height = (Math.random() * 20 + 10) + 'px';
        
        this.rainContainer.appendChild(raindrop);
        
        // 动画结束后重新创建雨滴
        setTimeout(() => {
            if (raindrop.parentNode) {
                raindrop.parentNode.removeChild(raindrop);
            }
            this.createRaindrop();
        }, (parseFloat(raindrop.style.animationDuration) + parseFloat(raindrop.style.animationDelay)) * 1000);
    }
    
    updateClearModeDisplay() {
        this.clearModeBtn.textContent = this.clearWithConfirm ? '🔒' : '🔓';
        this.clearModeBtn.title = this.clearWithConfirm ? '需要确认' : '无需确认';
    }
    
    toggleClearMode() {
        this.clearWithConfirm = !this.clearWithConfirm;
        this.updateClearModeDisplay();
        this.showNotification(this.clearWithConfirm ? '已切换至需要确认模式' : '已切换至无需确认模式');
    }
    
    enhancePunctuation() {
        const selection = window.getSelection();
        if (selection.rangeCount) {
            const range = selection.getRangeAt(0);
            const currentPos = range.startOffset;
            const text = this.editor.textContent;
            
            if (currentPos > 0 && text[currentPos-1] === '。') {
                // 在句号后添加空格
                const content = this.editor.innerHTML;
                const newContent = content.replace(/。/g, '。　　');
                if (content !== newContent) {
                    this.editor.innerHTML = newContent;
                }
            }
        }
    }
    
    showRandomQuote() {
        const randomQuote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
        this.quoteText.textContent = randomQuote;
        this.floatingQuote.classList.add('show');
        
        // 3秒后自动隐藏
        setTimeout(() => {
            this.floatingQuote.classList.remove('show');
        }, 3000);
    }
    
    showNotification(message) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(145deg, #8b4513, #654321);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        `;
        
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);
        
        // 3秒后移除
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new AncientWritingApp();
    
    // 添加一些动画效果
    const paper = document.querySelector('.paper');
    const inkwell = document.querySelector('.inkwell');
    
    // 纸张轻微摆动动画
    setInterval(() => {
        paper.style.transform = `rotate(${Math.sin(Date.now() * 0.001) * 0.5}deg)`;
    }, 50);
    
    // 墨盒滴水效果
    setInterval(() => {
        const inkDrop = document.querySelector('.ink-drop');
        if (inkDrop) {
            inkDrop.style.animation = 'none';
            setTimeout(() => {
                inkDrop.style.animation = 'dropFall 2s ease-in-out infinite';
            }, 100);
        }
    }, 4000);
});

// 添加一些音效提示（可选）
function playTypingSound() {
    // 创建键盘音效
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
}

// 监听键盘输入添加音效
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'DIV' && e.target.contentEditable === 'true') {
        playTypingSound();
    }
});