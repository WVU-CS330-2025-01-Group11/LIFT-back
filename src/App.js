import React, { useState } from 'react';
import data from './Data.json';
import 'bootstrap/dist/css/bootstrap.min.css';

function FetchData() {
    const [activeTab, setActiveTab] = useState(1); // State to manage active tab
    const [launches, setLaunches] = useState([]); // State to store launches
    const [name, setName] = useState(''); // State for launch name
    const [description, setDescription] = useState(''); // State for launch description

    // Function to handle saving a launch
    const handleSaveLaunch = () => {
        if (name && description) {
            const newLaunch = {
                id: launches.length + 1, // Unique ID for each launch
                name: name,
                description: description,
            };
            setLaunches([...launches, newLaunch]); // Add new launch to the list
            setName(''); // Clear the name field
            setDescription(''); // Clear the description field
        } else {
            alert('Please fill out both the name and description fields.');
        }
    };

    return (
        <div className="launchSites">
            <div className="tabs__above">
                <button
                    className={`tabs__button ${activeTab === 1 ? 'tabs__button--active' : ''}`}
                    onClick={() => setActiveTab(1)}
                >
                    Sites
                </button>
                <button
                    className={`tabs__button ${activeTab === 2 ? 'tabs__button--active' : ''}`}
                    onClick={() => setActiveTab(2)}
                >
                    Launches
                </button>
            </div>

            {/* Sites Tab */}
            <div className={`tabs__content ${activeTab === 1 ? 'tabs__content--active' : ''}`}>
                <h1>Sites</h1>
                <div className="d-flex flex-wrap">
                    {data.map((site, i) => (
                        <div className="border m-2 p-2" key={i} style={{ width: '30%' }}>
                            <h2>{site["Prefecture Name"]}</h2>
                            <p><strong>State:</strong> {site.State || 'N/A'}</p>
                            <p><strong>Zip Code:</strong> {site["Zip Code"] || 'N/A'}</p>
                            <p><strong>Elevation:</strong> {site.Elevation || 'N/A'}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Launches Tab */}
            <div className={`tabs__content ${activeTab === 2 ? 'tabs__content--active' : ''}`}>
                <h1>Launches</h1>
                <div className="mb-3">
                    <label htmlFor="launchName" className="form-label">Launch Name</label>
                    <input
                        type="text"
                        className="form-control"
                        id="launchName"
                        placeholder="Enter launch name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="launchDescription" className="form-label">Launch Description</label>
                    <textarea
                        className="form-control"
                        id="launchDescription"
                        rows="3"
                        placeholder="Enter launch description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    ></textarea>
                </div>
                <div className="mb-3">
                    <button className="btn btn-primary" onClick={handleSaveLaunch}>
                        Save Launch
                    </button>
                </div>

                {/* Display Saved Launches */}
                <div className="mt-4">
                    <h3>Saved Launches</h3>
                    {launches.length === 0 ? (
                        <p>No launches saved yet.</p>
                    ) : (
                        <ul className="list-group">
                            {launches.map((launch) => (
                                <li key={launch.id} className="list-group-item">
                                    <strong>{launch.name}</strong>
                                    <p>{launch.description}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
}

export default FetchData;