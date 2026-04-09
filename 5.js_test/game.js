// Web UI 数字猜谜游戏
class WebNumberGuessingGame {
    constructor() {
        this.targetNumber = this.generateRandomNumber();
        this.attempts = 0;
        this.maxAttempts = 10;
        this.gameOver = false;
        this.guessHistory = [];
        this.init();
    }

    // 生成1-100的随机数
    generateRandomNumber() {
        return Math.floor(Math.random() * 100) + 1;
    }

    // 初始化游戏
    init() {
        this.updateUI();
        this.setupEventListeners();
    }

    // 设置事件监听器
    setupEventListeners() {
        const guessInput = document.getElementById('guessInput');
        
        // 回车键支持
        guessInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.makeGuess();
            }
        });

        // 输入验证
        guessInput.addEventListener('input', (e) => {
            let value = parseInt(e.target.value);
            if (value > 100) e.target.value = 100;
            if (value < 1) e.target.value = 1;
        });
    }

    // 处理用户猜测
    makeGuess() {
        if (this.gameOver) {
            this.showResult('游戏已经结束！点击"重新开始"再来一局吧！', 'error');
            return;
        }

        const guessInput = document.getElementById('guessInput');
        const userGuess = parseInt(guessInput.value);

        // 输入验证
        if (isNaN(userGuess) || userGuess < 1 || userGuess > 100) {
            this.showResult('❌ 请输入1-100之间的有效数字！', 'error');
            return;
        }

        this.attempts++;
        this.guessHistory.push(userGuess);

        // 清空输入框
        guessInput.value = '';

        let resultMessage = '';
        let resultClass = '';

        if (userGuess === this.targetNumber) {
            this.gameOver = true;
            resultMessage = `🎉 恭喜！你猜对了！数字是 ${this.targetNumber}，用了 ${this.attempts} 次尝试。`;
            resultClass = 'success';
        } else if (this.attempts >= this.maxAttempts) {
            this.gameOver = true;
            resultMessage = `💔 游戏结束！正确答案是 ${this.targetNumber}。下次加油！`;
            resultClass = 'error';
        } else if (userGuess < this.targetNumber) {
            resultMessage = `📈 太小了！再试一次。你还剩 ${this.maxAttempts - this.attempts} 次机会。`;
            resultClass = 'info';
        } else {
            resultMessage = `📉 太大了！再试一次。你还剩 ${this.maxAttempts - this.attempts} 次机会。`;
            resultClass = 'info';
        }

        this.showResult(resultMessage, resultClass);
        this.updateHistory();
        this.updateUI();
    }

    // 显示结果
    showResult(message, className) {
        const resultElement = document.getElementById('result');
        resultElement.textContent = message;
        resultElement.className = 'result ' + className;
    }

    // 更新猜测历史
    updateHistory() {
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';

        this.guessHistory.forEach((guess, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            let status = '';
            if (guess === this.targetNumber) {
                status = '✅ 正确';
            } else if (guess < this.targetNumber) {
                status = '📈 太小';
            } else {
                status = '📉 太大';
            }

            historyItem.innerHTML = `
                <span>第 ${index + 1} 次: </span>
                <strong>${guess}</strong>
                <span> - ${status}</span>
            `;
            
            historyList.appendChild(historyItem);
        });

        // 滚动到底部
        historyList.scrollTop = historyList.scrollHeight;
    }

    // 更新UI状态
    updateUI() {
        const remainingElement = document.getElementById('remainingAttempts');
        const guessInput = document.getElementById('guessInput');
        const guessButton = document.querySelector('button[onclick="makeGuess()"]');

        remainingElement.textContent = this.maxAttempts - this.attempts;

        if (this.gameOver) {
            guessInput.disabled = true;
            guessButton.disabled = true;
        } else {
            guessInput.disabled = false;
            guessButton.disabled = false;
        }
    }

    // 重新开始游戏
    restartGame() {
        this.targetNumber = this.generateRandomNumber();
        this.attempts = 0;
        this.gameOver = false;
        this.guessHistory = [];
        
        const guessInput = document.getElementById('guessInput');
        guessInput.value = '';
        guessInput.focus();
        
        this.showResult('🔄 游戏已重新开始！猜一个1-100之间的数字。', 'info');
        this.updateHistory();
        this.updateUI();
    }

    // 获取游戏统计信息（用于扩展功能）
    getStats() {
        return {
            targetNumber: this.targetNumber,
            attempts: this.attempts,
            maxAttempts: this.maxAttempts,
            gameOver: this.gameOver,
            guessHistory: [...this.guessHistory]
        };
    }
}

// 创建游戏实例
let game;

// 页面加载完成后初始化游戏
document.addEventListener('DOMContentLoaded', function() {
    game = new WebNumberGuessingGame();
});

// 全局函数供HTML按钮调用
function makeGuess() {
    if (game) {
        game.makeGuess();
    }
}

function restartGame() {
    if (game) {
        game.restartGame();
    }
}

// 添加一些额外的功能
// 1. 提示功能（作弊模式）
function showHint() {
    if (game && !game.gameOver) {
        const stats = game.getStats();
        const range = Math.floor(stats.targetNumber / 10) * 10;
        alert(`💡 提示：数字在 ${range + 1} - ${range + 10} 之间`);
    }
}

// 2. 添加键盘快捷键
document.addEventListener('keydown', function(e) {
    if (e.key === 'r' || e.key === 'R') {
        restartGame();
    }
    if (e.key === 'h' || e.key === 'H') {
        showHint();
    }
});