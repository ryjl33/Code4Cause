import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';
import ballotLogo from './assets/ballotlogo.png';

interface CandidatesData {
  [candidate: string]: string;
}

function BallotPage() {
  // Retrieve address info passed from the form page
  const location = useLocation();
  const { street, city, state, zip } = location.state || {};
  
  const [candidates, setCandidates] = useState<CandidatesData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<any>(null);

  useEffect(() => {
    // Function to fetch the ballot data from the backend
    const fetchBallotData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/ask/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // Note: The backend expects the key "zipcode" instead of "zip"
          body: JSON.stringify({
            street: street,
            city: city,
            state: state,
            zipcode: zip,
          }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Expecting a JSON object with candidate names as keys
        const data: CandidatesData = await response.json();
        setCandidates(data);
        setLoading(false);
      } catch (err: any) {
        setError(err);
        setLoading(false);
      }
    };

    fetchBallotData();
  }, [street, city, state, zip]);

  return (
    <div className="ballot-container">
      <h1>Ballot Information</h1>
      <div className="address-info">
        <h3>Your Address:</h3>
        <p>{street}, {city}, {state} {zip}</p>
      </div>
      
      {loading ? (
        <p>Loading ballot data...</p>
      ) : error ? (
        <p>Error loading data: {error.message}</p>
      ) : (
        <div className="ballot-details">
          {Object.entries(candidates as CandidatesData).map(([name, description]) => (
            <div key={name} className="candidate-card">
              <h2>{name}</h2>
              <p>{description}</p>
            </div>
          ))}
        </div>
      )}

      {/* Logo in the bottom-left corner */}
      <img src={ballotLogo} alt="Our Logo" className="bottom-logo" />
    </div>
  );
}

export default BallotPage;