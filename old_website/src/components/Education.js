import React from 'react';
import { Typography, Container, Box } from '@mui/material';

function Education() {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Education
        </Typography>
        <Box my={2}>
          <Typography variant="h5" component="h2">
            Bachelors of Technology
          </Typography>
          <Typography variant="body1">Major in Computer Science, Minor in Psychology</Typography>
          <Typography variant="body2">Amity University, 08/2016 - 08/2020</Typography>
        </Box>
      </Box>
    </Container>
  );
}

export default Education;
