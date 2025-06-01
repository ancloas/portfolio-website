import React from 'react';
import { Typography, Container, Box, Grid, Card, CardContent } from '@mui/material';
import './Projects.css'; // Import the stylesheet

function Projects() {
  const projectData = [
    {
      title: "Blog Project",
      description: "Developed a Python and Django blog with rich-text post creation, user authentication, post interaction, guest post management, analytics, and multiple views.",
    //   image: "path/to/image1.jpg" // Add image path if needed
    },
    {
      title: "LinkedIn Data Mining Project",
      description: "Built a generic python project to mine data for organizations and employees to identify hiring trends.",
    //   image: "path/to/image2.jpg" // Add image path if needed
    },
    {
      title: "Crime Data Analysis",
      description: "Analyzed a crime dataset to perform EDA and identified factors affecting crimes against women in India.",
    //   image: "path/to/image3.jpg" // Add image path if needed
    },
    {
      title: "Battle Tank Game",
      description: "Created a 2D battle tank game using C++ and OOP concepts, implementing vector addition and collision theory.",
    //   image: "path/to/image4.jpg" // Add image path if needed
    },
    {
      title: "Ball vs. Wall Game",
      description: "Developed a single-player Arkanoid styled game using C++ and OOP concepts, applying physics for movement and collisions.",
    //   image: "path/to/image5.jpg" // Add image path if needed
    },
  ];

  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom className="projects-heading">
          Projects
        </Typography>
        <Grid container spacing={4}>
          {projectData.map((project, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card variant="outlined" className="project-card">
                {project.image && (
                  <img src={project.image} alt={project.title} className="project-image" />
                )}
                <CardContent>
                  <Typography variant="h6" gutterBottom className="project-title">
                    {project.title}
                  </Typography>
                  <Typography variant="body1" className="project-description">
                    {project.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default Projects;
