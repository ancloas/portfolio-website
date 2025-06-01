import React from 'react';
import { Link } from 'react-router-dom';
import { Typography, Container, Box, Button, Grid } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';
import SocialMediaIcons from './SocialMediaIcons'; // Import the new component
import './Home.css';

function Home() {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Hey! I am Anugrah.
        </Typography>
        <Typography variant="h5" component="p" gutterBottom>
          A driven data professional and GenAI developer.
        </Typography>
        <Typography variant="body1" component="p" gutterBottom>
          This is my personal website where you can find my projects, skills, and more about my journey.
        </Typography>
        <Typography variant="body1" component="p">
          Feel free to explore my <Link to="/about" className="link">about</Link> page, check out my <Link to="/projects" className="link">projects</Link>, or <Link to="/contact" className="link">contact</Link> me.
        </Typography>
        
        <SocialMediaIcons />
      </Box>
    </Container>
  );
}

export default Home;
