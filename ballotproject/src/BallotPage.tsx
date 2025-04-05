import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';
import ballotLogo from './assets/ballotlogo.png';

interface BallotData {
  president: string;
  vicePresident: string;
  secretary: string;
  treasurer: string;
}

function BallotPage() {
  const location = useLocation();
  // Optionally retrieve the address passed from the form
  const addressData = location.state;
  const [ballotData, setBallotData] = useState<BallotData | null>(null);

  useEffect(() => {
    // Replace this dummy data with an actual fetch call to your Flask backend when ready.
    // Example:
    // fetch('http://localhost:5000/api/ballot', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(addressData)
    // })
    // .then(res => res.json())
    // .then(data => setBallotData(data));
    const dummyData: BallotData = {
      president: "Candidate A",
      vicePresident: "Candidate B",
      secretary: "Candidate C",
      treasurer: "Candidate D"
    };
    setTimeout(() => {
      setBallotData(dummyData);
    }, 500);
  }, [addressData]);

  return (
    <div className="ballot-container">
      <h1>Ballot Information</h1>
      {addressData && (
        <div className="address-info">
          <h3>Your Address:</h3>
          <p>{addressData.street}, {addressData.city}, {addressData.state} {addressData.zip}</p>
        </div>
      )}
      {ballotData ? (
        <div className="ballot-details">
          <div>
            <h2>President</h2>
            <p>{ballotData.president}</p>
          </div>
          <div>
            <h2>Vice President</h2>
            <p>{ballotData.vicePresident}</p>
          </div>
          <div>
            <h2>Secretary</h2>
            <p>{ballotData.secretary}</p>
          </div>
          <div>
            <h2>Treasurer</h2>
            <p>{ballotData.treasurer}</p>
          </div>
        </div>
      ) : (
        <p>Loading ballot data...</p>
      )}

      {/* Logo at bottom-left */}
      <img src={ballotLogo} alt="Our Logo" className="bottom-logo" />
      
    </div>
  );
}

export default BallotPage;