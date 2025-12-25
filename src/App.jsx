import React from 'react'
import { Routes, Route, useNavigate } from 'react-router-dom'
import './App.css'
import Start from './pages/Start'

function Home() {
  const navigate = useNavigate()
  
  const options = [
    { id: 1, name: '四级核心词', level: 'CET4' },
    { id: 2, name: '六级核心词', level: 'CET6' },
    // 预留空间，后续可扩展至10个左右
    { id: 3, name: '' },
    { id: 4, name: '' },
    { id: 5, name: '' },
    { id: 6, name: '' },
    { id: 7, name: '' },
    { id: 8, name: '' },
    { id: 9, name: '' },
    { id: 10, name: '' },
  ]

  const handleOptionClick = (option) => {
    if (option.name && option.level) {
      navigate(`/start?level=${option.level}`)
    }
  }

  return (
    <div className="app">
      <div className="header-buttons">
        <a
          href="https://github.com/wwcxin/Recite"
          target="_blank"
          rel="noopener noreferrer"
          className="header-btn"
        >
          项目地址
        </a>
        <a
          href="mailto:hi@b23.run"
          className="header-btn"
        >
          联系
        </a>
      </div>
      <div className="container">
        <h1 className="title">大开门识单词</h1>
        
        <div className="image-container">
          <img src="/image/Cover.png" alt="封面" className="cover-image" />
        </div>

        <div className="options-grid">
          {options.map((option) => (
            <div
              key={option.id}
              className={`option-card ${option.name ? 'active' : 'placeholder'}`}
              onClick={() => handleOptionClick(option)}
            >
              {option.name || <span className="placeholder-text">预留</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/start" element={<Start />} />
    </Routes>
  )
}

export default App

