import React from 'react';
import { Typography, Container, Box } from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent
} from '@mui/lab';
import './Experience.css';

const experiences = [
  {
    title: 'Software Engineering Intern at MAQ Software',
    date: '01/2020 - 07/2020',
    responsibilities: [
      'Designed Azure Data Lake storage and Azure SQL Databases and schemas.',
      'Worked on Migration of existing code to Azure Databricks as part of a Cloud Migration Project.',
      'Designed ETL pipelines to migrate data from On-premise to Cloud using Azure Data Factory.'
    ]
  },
  {
    title: 'Software Engineer 1 at MAQ Software',
    date: '07/2020 - 08/2021',
    responsibilities: [
      'Developed and deployed enterprise applications with C++, Python, SQL Server, and Azure as backend developer.',
      'Worked on implementing and optimizing the existing codebase to improve the performance of the created applications.',
      'Designed and developed ETL pipelines using ADF to facilitate Big Data Ingestion and developed and transformed the data using Azure Databricks.',
      'Demonstrated ability to work in team and help interns and new team members in learning the SDLC and code architecture.'
    ]
  },
  {
    title: 'Data Engineering Analyst at Accenture',
    date: '08/2021 - Current',
    responsibilities: [
      'Designed, developed, and deployed Django-based web application utilizing OpenAI and Lang-Chain.',
      'Leveraged OpenAI and Lang-Chain technologies to develop an advanced chatbot.',
      'Developed an LLM chatbot to use Python and NLP techniques to automate customer support interactions.',
      'Developed a synthetic data generation framework using Python, Flask architecture and data manipulation libraries.'
    ]
  }
];

const Experience = () => {
  return (
    <Container>
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Experience
        </Typography>
        <Timeline position="alternate">
          {experiences.reverse().map((experience, index) => (
            <TimelineItem key={index}>
              <TimelineOppositeContent sx={{ m: 'auto 0' }}>
                <Typography variant="body2" color="text.secondary">
                  {experience.date}
                </Typography>
              </TimelineOppositeContent>
              <TimelineSeparator>
                <TimelineDot />
                {index !== experiences.length - 1 && <TimelineConnector />}
              </TimelineSeparator>
              <TimelineContent sx={{ py: '12px', px: 2 }} className='timeline-content'>
                <Typography variant="h5" component="h2">
                  {experience.title}
                </Typography>
                <ul>
                  {experience.responsibilities.map((responsibility, idx) => (
                    <li key={idx}>
                      <Typography variant="body2">{responsibility}</Typography>
                    </li>
                  ))}
                </ul>
              </TimelineContent>
            </TimelineItem>
          ))}
        </Timeline>
      </Box>
    </Container>
  );
};

export default Experience;
