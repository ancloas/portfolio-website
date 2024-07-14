import React from 'react';
import { Link } from 'react-router-dom';
import { Typography, Container, Box, Button, Grid } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';
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
        
        <Box my={4}>
          <Typography variant="h6">Connect with me:</Typography>
          <Grid container spacing={2}>
            <Grid item>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<LinkedIn />}
                component="a"
                href="https://www.linkedin.com/in/yourprofile"
                target="_blank"
              >
                LinkedIn
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<GitHub />}
                component="a"
                href="https://github.com/yourprofile"
                target="_blank"
              >
                GitHub
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<Facebook />}
                component="a"
                href="https://www.facebook.com/yourprofile"
                target="_blank"
              >
                Facebook
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                color="primary"
                startIcon={<Twitter />}
                component="a"
                href="https://twitter.com/yourprofile"
                target="_blank"
              >
                Twitter
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}

export default Home;
