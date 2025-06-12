import { useState } from 'react'
import './App.css'
import Login from './Components/Login.jsx'
import Home from './Components/Home.jsx'
import About from './Components/About.jsx'
// import Projects from './Components/Projects.jsx'
// import Contact from './Components/Contact.jsx'
// import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
// import Navbar from './Components/Navbar.jsx'
// import Footer from './Components/Footer.jsx'
// import Skills from './Components/Skills.jsx'
// import Testimonials from './Components/Testimonials.jsx'
// import Services from './Components/Services.jsx'
// import TestimonialsCard from './Components/TestimonialsCard.jsx'
// import TestimonialsCard2 from './Components/TestimonialsCard2.jsx'
// import TestimonialsCard3 from './Components/TestimonialsCard3.jsx'
// import TestimonialsCard4 from './Components/TestimonialsCard4.jsx'
// import TestimonialsCard5 from './Components/TestimonialsCard5.jsx'
// import TestimonialsCard6 from './Components/TestimonialsCard6.jsx'
// import TestimonialsCard7 from './Components/TestimonialsCard7.jsx'       

function App() {
  // const [count, setCount] = useState(0)

  return (
     <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Welcome to My Portfolio
        </h2> 
      <Login />
    </div>
      </div>
  )
}

export default App
  