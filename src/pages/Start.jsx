import React, { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import '../styles/Start.css'

function Start() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const level = searchParams.get('level') // 'CET4' or 'CET6'
  
  const [words, setWords] = useState([])
  const [currentWord, setCurrentWord] = useState(null)
  const [options, setOptions] = useState([])
  const [score, setScore] = useState(0)
  const [isShaking, setIsShaking] = useState(true)
  const [selectedImage, setSelectedImage] = useState('wait')
  const [isFirstTry, setIsFirstTry] = useState(true)
  const [isAnswered, setIsAnswered] = useState(false)
  const [showSuccessTip, setShowSuccessTip] = useState(false)
  
  const audioRef = useRef(null)
  const successAudioRef = useRef(null)
  const success2AudioRef = useRef(null)

  // 加载题库
  useEffect(() => {
    const loadWords = async () => {
      try {
        const fileName = level === 'CET4' ? 'CET4luan_1.json' : 'CET6luan_1.json'
        const response = await fetch(`/json/${fileName}`)
        const data = await response.json()
        setWords(data)
      } catch (error) {
        console.error('加载题库失败:', error)
      }
    }
    
    if (level && (level === 'CET4' || level === 'CET6')) {
      loadWords()
    } else {
      navigate('/')
    }
  }, [level, navigate])

  // 获取随机单词
  const getRandomWord = useCallback(() => {
    if (words.length === 0) return null
    const randomIndex = Math.floor(Math.random() * words.length)
    return words[randomIndex]
  }, [words])

  // 获取随机错误选项
  const getRandomWrongOptions = useCallback((correctTranCn, count = 2) => {
    const wrongOptions = []
    const usedIndices = new Set()
    
    while (wrongOptions.length < count && usedIndices.size < words.length) {
      const randomIndex = Math.floor(Math.random() * words.length)
      if (!usedIndices.has(randomIndex)) {
        usedIndices.add(randomIndex)
        const word = words[randomIndex]
        if (word.tranCn && word.tranCn !== correctTranCn) {
          wrongOptions.push(word.tranCn)
        }
      }
    }
    
    return wrongOptions
  }, [words])

  // 加载新题目
  const loadNewQuestion = useCallback(() => {
    const word = getRandomWord()
    if (!word) return

    setCurrentWord(word)
    setIsFirstTry(true)
    setIsAnswered(false)
    setIsShaking(true)
    setSelectedImage('wait')

    // 生成选项
    const correctOption = word.tranCn
    const wrongOptions = getRandomWrongOptions(correctOption, 2)
    const allOptions = [correctOption, ...wrongOptions]
    
    // 随机打乱选项顺序
    const shuffledOptions = allOptions.sort(() => Math.random() - 0.5)
    setOptions(shuffledOptions)

    // 播放单词音频
    if (word.usspeech) {
      setTimeout(() => {
        playWordAudio(word.usspeech)
      }, 300)
    }
  }, [getRandomWord, getRandomWrongOptions])

  // 播放单词音频
  const playWordAudio = (usspeech) => {
    if (audioRef.current) {
      const audioUrl = `https://dict.youdao.com/dictvoice?audio=${usspeech}`
      audioRef.current.src = audioUrl
      audioRef.current.play().catch(err => console.error('播放音频失败:', err))
    }
  }

  // 处理选项选择
  const handleOptionClick = (option, position) => {
    if (isAnswered) return

    setIsAnswered(true)
    setIsShaking(false)

    // 根据位置设置图片
    if (position === 0) {
      setSelectedImage('left')
    } else if (position === 1) {
      setSelectedImage('center')
    } else {
      setSelectedImage('right')
    }

    const isCorrect = option === currentWord.tranCn

    if (isCorrect) {
      // 答对了
      // 显示提示框
      setShowSuccessTip(true)
      setTimeout(() => {
        setShowSuccessTip(false)
      }, 2000)
      
      if (isFirstTry) {
        // 一次答对
        setScore(prev => prev + 1)
        if (success2AudioRef.current) {
          success2AudioRef.current.play().catch(err => console.error('播放音频失败:', err))
        }
      } else {
        // 非一次答对
        setScore(prev => prev + 1)
        if (successAudioRef.current) {
          successAudioRef.current.play().catch(err => console.error('播放音频失败:', err))
        }
      }
      
      // 延迟后加载新题目
      setTimeout(() => {
        loadNewQuestion()
      }, 1500)
    } else {
      // 答错了
      setIsFirstTry(false)
      setScore(prev => Math.max(0, prev - 1))
      
      // 播放题目单词语音
      if (currentWord.usspeech) {
        setTimeout(() => {
          playWordAudio(currentWord.usspeech)
        }, 500)
      }
      
      // 恢复等待状态
      setTimeout(() => {
        setIsShaking(true)
        setSelectedImage('wait')
        setIsAnswered(false)
      }, 2000)
    }
  }

  // 初始化加载题目
  useEffect(() => {
    if (words.length > 0 && !currentWord) {
      loadNewQuestion()
    }
  }, [words, currentWord, loadNewQuestion])

  // 获取当前显示的图片
  const getCurrentImage = () => {
    switch (selectedImage) {
      case 'left':
        return '/image/left.png'
      case 'center':
        return '/image/center.png'
      case 'right':
        return '/image/right.png'
      default:
        return '/image/wait.png'
    }
  }

  if (!currentWord) {
    return (
      <div className="start-page">
        <div className="loading">加载中...</div>
      </div>
    )
  }

  return (
    <div className="start-page">
      {/* 左上角返回按钮 */}
      <button className="back-button" onClick={() => navigate('/')}>
        ← 返回
      </button>

      {/* 右上角计数 */}
      <div className="score-container">
        <img src="/image/great.png" alt="great" className="score-image" />
        <span className="score-text">× {score}</span>
      </div>

      {/* 答对提示框 */}
      {showSuccessTip && (
        <div className="success-tip">
          蒸蚌+1
        </div>
      )}

      {/* 单词和音频按钮 */}
      <div className="word-container">
        <span className="word-label">GB</span>
        <span className="word-text">{currentWord.headWord}</span>
        {currentWord.usspeech && (
          <button
            className="audio-button"
            onClick={() => playWordAudio(currentWord.usspeech)}
          >
            🔊
          </button>
        )}
      </div>

      {/* 中间图片 */}
      <div className={`image-wrapper ${isShaking ? 'shaking' : ''}`}>
        <img src={getCurrentImage()} alt="状态" className="status-image" />
      </div>

      {/* 提示文字 */}
      <div className="hint-text">请选择正确的中释：</div>

      {/* 选项按钮 */}
      <div className="options-container">
        {options.map((option, index) => {
          let positionClass = ''
          if (index === 0) positionClass = 'option-left'
          else if (index === 1) positionClass = 'option-center'
          else positionClass = 'option-right'

          const isCorrect = option === currentWord.tranCn
          const isSelected = isAnswered && (
            (index === 0 && selectedImage === 'left') ||
            (index === 1 && selectedImage === 'center') ||
            (index === 2 && selectedImage === 'right')
          )
          
          return (
            <button
              key={index}
              className={`option-button ${positionClass} ${
                isAnswered && isCorrect ? 'correct' : ''
              } ${isAnswered && !isCorrect && isSelected ? 'wrong' : ''}`}
              onClick={() => handleOptionClick(option, index)}
              disabled={isAnswered}
            >
              {option}
            </button>
          )
        })}
      </div>

      {/* 音频元素 */}
      <audio ref={audioRef} preload="auto" />
      <audio ref={successAudioRef} src="/voice/great.mp3" preload="auto" />
      <audio ref={success2AudioRef} src="/voice/great2.mp3" preload="auto" />
    </div>
  )
}

export default Start

