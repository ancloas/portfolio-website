import React from 'react';
import { Typography, Container, Box, Grid, Paper } from '@mui/material';
import { styled } from '@mui/system';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import ArticleIcon from '@mui/icons-material/Article';
import BadgeIcon from '@mui/icons-material/Badge';
import SchoolIcon from '@mui/icons-material/School';

const StyledPaper = styled(Paper)({
  padding: '20px',
  borderRadius: '8px',
  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  display: 'flex',
  alignItems: 'center',
});

const activities = [
  {
    icon: <SchoolIcon />,
    title: "100 Days of Code: Python Pro Bootcamp",
    description: "Completed Udemy certification."
  },
  {
    icon: <BadgeIcon />,
    title: "Microsoft Certified: Azure Fundamentals",
    description: "Earned certification for Azure fundamentals."
  },
  {
    icon: <SportsEsportsIcon />,
    title: "Chess Tournament",
    description: "Won Second Place in Indore UICC chess tournament."
  },
  {
    icon: <ArticleIcon />,
    title: "Medium Articles",
    description: "Wrote and published 5 articles on various topics."
  },
  {
    icon: <BadgeIcon />,
    title: "HackerRank Badges",
    description: "Earned 5-star Gold Badges in Problem Solving, C++, and SQL challenges."
  },
  {
    icon: <BadgeIcon />,
    title: "Advanced Data Analysis",
    description: "Completed certification from Vanderbilt University."
  },
  {
    icon: <BadgeIcon />,
    title: "Generative AI with LLMs",
    description: "Completed certification from DeepLearning.AI and AWS."
  },
  {
    icon: <BadgeIcon />,
    title: "Prompt Engineering Specialization",
    description: "Completed certification from Vanderbilt University."
  }
];

function Extracurricular() {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Extracurricular Activities
        </Typography>
        <Grid container spacing={4}>
          {activities.map((activity, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <StyledPaper>
                <Box sx={{ mr: 2, fontSize: '2rem', color: '#ff9900' }}>
                  {activity.icon}
                </Box>
                <Box>
                  <Typography variant="h6">{activity.title}</Typography>
                  <Typography variant="body2">{activity.description}</Typography>
                </Box>
              </StyledPaper>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default Extracurricular;
