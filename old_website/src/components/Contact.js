import React from 'react';
import { Typography, Container, Box, Button, Grid } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';
import SocialMediaIcons from './SocialMediaIcons';

function Contact() {
  return (
    <Container>
      <Box my={4}>  
        <Typography variant="body1" gutterBottom>
          You can connect with me by clicking any of the following links.
        </Typography>
        <br />
      <SocialMediaIcons />

        <Typography variant="body1" gutterBottom>
          You can also reach me via email at: <strong>anugrahgupta.52@gmail.com</strong>
        </Typography>
      </Box>
    </Container>
  );
}

export default Contact;
