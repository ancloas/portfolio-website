import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { NavLink } from 'react-router-dom';
import { styled } from '@mui/system';

const StyledAppBar = styled(AppBar)({
  background: 'linear-gradient(to right, #ff9900 0%, #000066 51%)', 
  boxShadow: 'none',
  position: 'fixed', // Keep it fixed
  top: 0,
  left: 0,
  right: 0,
  zIndex: 1000, // Ensure it stays on top
});

const StyledButton = styled(Button)(({ theme }) => ({
  color: 'white',
  fontSize: '1.1rem',
  textTransform: 'none',
  '&.active': {
    fontWeight: 'bold',
    borderBottom: '2px solid white',
  },
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
}));

const Navbar = () => {
  const links = [
    { to: '/', label: 'Home' },
    { to: '/about', label: 'About' },
    { to: '/skills', label: 'Skills' },
    { to: '/experience', label: 'Experience' },
    { to: '/projects', label: 'Projects' },
    // { to: '/education', label: 'Education' },
    { to: '/extracurricular', label: 'Extracurricular' },
    { to: '/contact', label: 'Contact' },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <StyledAppBar>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h4" sx={{ flexGrow: 1, fontFamily: 'Roboto, sans-serif' }}>
            Anugrah Gupta
          </Typography>
          <Box>
            {links.map(({ to, label }) => (
              <StyledButton key={to} component={NavLink} to={to} activeClassName="active">
                {label}
              </StyledButton>
            ))}
          </Box>
        </Toolbar>
      </StyledAppBar>
    </Box>
  );
};

export default Navbar;
