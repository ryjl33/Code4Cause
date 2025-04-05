import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AddressForm from './AddressForm';
import BallotPage from './BallotPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AddressForm />} />
        <Route path="/ballot" element={<BallotPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;