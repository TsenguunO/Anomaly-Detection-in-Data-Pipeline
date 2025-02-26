import { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Container, Row, Button, Col, Alert } from 'react-bootstrap';
import PipelineSideBar from '../../components/PipelineSidebar';

const UpdateDataSetPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const [imageSrc, setImageSrc] = useState('/empty.png');
    const [file, setFile] = useState('');
    const [uploadSuccess, setUploadSuccess] = useState(false);

    if (!loggedInStatus) {
        history.push('/login');
    }

    const handleFileChange = (event) => {
        const newFile = event.target.files[0];
        if (newFile) {
            setFile(newFile);
        }
    };

    const handleUploadClick = () => {
        if (file) {
            console.log('Uploading file:', file);
            setImageSrc('/csv.png');
            setUploadSuccess(true);
            setTimeout(() => {
                setUploadSuccess(false);
            }, 3000);
        } else {
            alert('No file selected!');
        }
    };

    const handleNextButtonClick = () => {
        history.push('/pipeline/data');
    };

    return (
        <Container fluid className="update-dataset-page-container">
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <PipelineSideBar />
                </Col>
                <Col xs={10} id="page-content-wrapper">
                    <Row className="justify-content-md-center">
                        <h1>Upload new data to dataset</h1>
                    </Row>
                    <Row className="justify-content-md-center">
                        <Col md={8} className="text-center">
                            <img src={imageSrc} alt="CSV preview" className='csv' />
                            <div className="my-3">
                                <input type="file" className='select-file-button' onChange={handleFileChange} />
                            </div>
                        </Col>
                    </Row>
                    <Row className="justify-content-md-center">
                        {uploadSuccess && <Col md={8} className="text-center"><Alert variant="success">Upload successfully!</Alert></Col>}
                    </Row>
                    <Row className="justify-content-md-center mt-3">
                        <Col md={4} className="text-right">
                            <Button style={{ minWidth: '120px' }} onClick={handleUploadClick}>Upload a file</Button>
                        </Col>
                        <Col md={4} className="text-left" style={{ paddingLeft: '80px' }}>
                            <Button onClick={handleNextButtonClick}>Next</Button>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
}

export default UpdateDataSetPage;
