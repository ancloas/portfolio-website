// SocialMediaIcons.js
import React from 'react';
import { Button, Grid, Box } from '@mui/material';
import { Facebook, LinkedIn, GitHub, Twitter } from '@mui/icons-material';

const SocialMediaIcons = () => {
  return (
    <Box my={2}> {/* Add margin to the Box */}
      <Grid container spacing={2}>
        <Grid item>
          <Button
            variant="outlined"
            color="primary"
            startIcon={<LinkedIn />}
            component="a"
            href="https://www.linkedin.com/in/anugrah-vardhan-gupta-67531112a/"
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
            href="https://github.com/ancloas"
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
            href="https://www.facebook.com/anugrah.gupta.39/"
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
            href="https://twitter.com/AnugrahGup430"
            target="_blank"
          >
            Twitter
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SocialMediaIcons;
