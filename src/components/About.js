import React from 'react';
import { Typography, Container, Box, Button, Grid } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';

function About() {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          About Me
        </Typography>
        <Typography variant="body1" component="p" gutterBottom>
          <li>I’m a programmer with combined professional experience of more than 4 years in Data Engineering and Software Engineering, allowing me to grasp best of both worlds.</li>
          <li>I got to learn and play with tools like ADB, ADF, experienced the power of SQL, NoSQL, and Pandas in data analysis in my data engineering experience.</li>
          <li> while my Software Engineering experience allowed me to build a solid foundation in web application development with HTML, CSS, and JavaScript, creation of dynamic Web APIs using frameworks like Django and Flask, along with exploring the capabilities of React and its components.</li>
          <li>But the happiest and favouirte task in all of my computer Science experience is when I used to loose myself while solving problems on HackerRank and realize it's midnight already.</li>
        </Typography>
        <Typography variant="body1" component="p" gutterBottom>
          <li>When I’m not coding, I’m sharing my thoughts through writing on Medium. I believe in sharing knowledge and insights, making it easier for others to navigate their own paths.</li>
        </Typography>
        <Typography variant="body1" component="p">
          <li>Chess is another passion of mine—it’s not a profession, but rather a mental battleground where I sharpen my problem-solving skills. 
          With a competitive rating of 1611, it keeps me thinking strategically and creatively. Chess teaches me new ways to approach challenges, and I love the thrill of the game.</li>
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

export default About;
