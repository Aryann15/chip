import './App.css';
import {Route, Routes , Link} from "react-router-dom"
import Review from './pages/Review';
import Home from './pages/Home';

function App() {
  return <div>
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/review">Review</Link>
        </li>
      </ul>
    </nav>

    <Routes>
      <Route path ="/" element={<Home/>}/>
      <Route path ="/review" element={<Review />}/>

    </Routes>

  </div>
}

export default App;
