import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Row, Col, Container } from 'react-bootstrap';
import SideBar from '../../components/Sidebar';

const ViewPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const [dropdownData, setDropdownData] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState('');
    const [csvPreview, setCsvPreview] = useState(null);
    const [email,setEmail] = useState(localStorage.getItem('email'));
    useEffect(() => {
        listDatasetsApi();
    }, []);
    
    const listDatasetsApi = async () => {
        // event.preventDefault();
        const url = 'http://localhost:8000/api/dataset/list_user_datasets';
        const response = await fetch(url, {
          method: 'post',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify({
            email
          }),
        });
        const data = await response.json();
        if (data.error) {
          // errorDialog
          alert(data.error)
        } else {
          // localStorage.setItem('token', data.token)
          // localStorage.setItem('email', email)
          // props.setToken(data.token);
          // navigate('/dashboard');
          // navigate('/');
          console.log(data.tables)
          setDropdownData(data.tables)
        //   return 
        }
      }

    return (
        <Container className="view-page-container">
            <Row>
                <Col className="col-2">
                    <SideBar />
                </Col>
                <Col className="col-10">
                    <h1>Data View Page</h1>
                    <div className="data-selection">
                        <h2>Select a dataset to preview</h2>
                        <div className="dropdown-bar">
                            <select 
                                className="dataset-select"
                                onChange={(e) => setSelectedDataset(e.target.value)}
                                value={selectedDataset}
                            >
                                <option value="">Select a dataset</option>
                                {dropdownData.map((item, index) => (
                                    <option key={index} value={item}>
                                        {item}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="csv-preview">
                        {selectedDataset && csvPreview ? (
                            <pre>{csvPreview}</pre>
                        ) : (
                            <div>No dataset selected</div>
                        )}
                    </div>
                </Col>
            </Row>
        </Container>
    );
}

export default ViewPage;

