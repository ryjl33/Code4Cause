import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';
import sealImg from './assets/seal.png';
import ballotLogo from './assets/ballotlogo.png';

function AddressForm() {
  const [form, setForm] = useState({
    street: '',
    city: '',
    state: '',
    zip: ''
  });

  const navigate = useNavigate();

  // Check that all fields are non-empty
  const isFormComplete =
    form.street.trim() !== "" &&
    form.city.trim() !== "" &&
    form.state.trim() !== "" &&
    form.zip.trim() !== "";

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Navigate to the ballot page and pass the address info via state.
    navigate('/ballot', { state: form });
  };

  return (
    <div className="container">
      <div className="overlay">
        <img src={sealImg} alt="Seal" className="seal" />
        <h1>Enter Your Address</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="street"
            placeholder="Street Address"
            value={form.street}
            onChange={handleChange}
          />
          <input
            type="text"
            name="city"
            placeholder="City"
            value={form.city}
            onChange={handleChange}
          />
          <input
            type="text"
            name="state"
            placeholder="State (2-letter)"
            maxLength={2}
            value={form.state}
            onChange={handleChange}
          />
          <input
            type="text"
            name="zip"
            placeholder="ZIP Code"
            value={form.zip}
            onChange={handleChange}
          />
          {/* Disable button unless the form is complete */}
          <button type="submit" disabled={!isFormComplete} className={isFormComplete ? 'active' : ''}>
            Enter
          </button>
        </form>
      </div>
      {/* Logo at bottom-left */}
      <img src={ballotLogo} alt="Our Logo" className="bottom-logo" />
    </div>
  );
}

export default AddressForm;