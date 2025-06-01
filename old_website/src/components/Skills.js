import React, { useState } from 'react';
import { Box, Tabs, Tab, Chip, Typography } from '@mui/material';
import { styled } from '@mui/system';
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import './Skills.css';

const skillsData = {
  'Data Science and Analysis': [
    'Machine Learning (ML)',
    'Large Language Model (LLM)',
    'OpenAI',
    'Natural Language Processing (NLP)',
    'Business Intelligence',
    'Pandas',
    'Lang-Chain',
    'Prompt Engineering'
  ],
  'Programming Languages': [
    'C++',
    'Python',
    'JavaScript'
  ],
  'Data Technologies': [
    'SQL Server',
    'MySQL',
    'Azure',
    'MongoDB',
    'NoSQL',
    'Pandas',
    'NumPy',
    'PySpark',
    'ETL',
    'Data Modeling',
    'Data Warehousing',
    'Azure Databricks',
    'Azure Data Factory',
    'Azure Data Lake Storage',
    'Azure Functions'
  ],
  'Web Development': [
    'Django',
    'Flask',
    'HTML',
    'CSS'
  ],
  'Version Control and CI/CD': [
    'Git',
    'Bitbucket',
    'GitHub',
    'Azure Git',
    'Docker'
  ],
  'Software Development Methodologies': [
    'Object-Oriented Programming (OOP)',
    'Software Development Lifecycle (SDLC)'
  ]
};

const StyledTab = styled(Tab)({
  textTransform: 'none',
  fontWeight: 'bold',
  fontSize: '1rem',
  alignItems: 'flex-start',
  padding: '10px 20px',
  '&.Mui-selected': {
    background: 'linear-gradient(90deg, rgba(28,113,201,1) 51%, rgba(255,89,0,1) 100%)',
    borderRadius: '10px 0 0 10px',
    color: '#fff'
  }
});

const Skills = () => {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'row', width: '100%', padding: '20px' }}>
      <Tabs
        orientation="vertical"
        value={selectedTab}
        onChange={handleChange}
        aria-label="skills tabs"
        sx={{ borderRight: 1, borderColor: 'divider', minWidth: '200px' }}
      >
        {Object.keys(skillsData).map((category, index) => (
          <StyledTab key={index} label={category} />
        ))}
      </Tabs>
      <Box sx={{ flexGrow: 1, padding: '20px' }}>
        <TransitionGroup>
          {Object.keys(skillsData).map((category, index) => (
            <CSSTransition
              key={index}
              in={selectedTab === index}
              timeout={300}
              classNames="fade"
              unmountOnExit
            >
              <Box role="tabpanel">
                {selectedTab === index && (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '20px' }}>
                    {skillsData[category].map((skill, idx) => (
                      <Chip key={idx} label={skill} variant="outlined" sx={{ fontSize: '1rem', fontWeight: 'bold' }} />
                    ))}
                  </Box>
                )}
              </Box>
            </CSSTransition>
          ))}
        </TransitionGroup>
      </Box>
    </Box>
  );
};

export default Skills;
