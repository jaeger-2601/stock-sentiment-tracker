import { Outlet } from 'react-router-dom';

import '../css/App.css';

import CustomNavbar from './Navbar';

function App() {
  return (
    <div className="App">
      <header>
        <CustomNavbar/>
      </header>
      
      <div id="detail">
        <Outlet />
      </div>
    </div>
  );
}

export default App;
