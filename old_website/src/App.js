import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from '@mui/material';
import Navbar from './components/Navbar';
import Home from './components/Home';
import About from './components/About';
import Skills from './components/Skills';
import Experience from './components/Experience';
import Projects from './components/Projects';
// import Education from './components/Education';
import Extracurricular from './components/Extracurricular';
import Contact from './components/Contact';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Container sx={{ marginTop: '70px' }}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/skills" element={<Skills />} />
        <Route path="/experience" element={<Experience />} />
        <Route path="/projects" element={<Projects />} />
        {/* <Route path="/education" element={<Education />} /> */}
        <Route path="/extracurricular" element={<Extracurricular />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
      </Container>
    </Router>
  );
};

export default App;
