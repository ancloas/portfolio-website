import React from 'react';
import { Typography, Container, Box, Button, Grid } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';

function Contact() {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Contact
        </Typography>
        <Typography variant="body1" gutterBottom>
          Feel free to reach out through any of the following platforms:
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
        
        <Typography variant="body1" gutterBottom>
          You can also reach me via email at: <strong>anugrahgupta.52@gmail.com</strong>
        </Typography>
      </Box>
    </Container>
  );
}

export default Contact;
