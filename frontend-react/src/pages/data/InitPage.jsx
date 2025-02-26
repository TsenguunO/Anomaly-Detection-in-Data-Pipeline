import { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore } from "../../stores";
import { Row, Col, Container } from 'react-bootstrap';
import SideBar from '../../components/Sidebar';


const InitPage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const loggedInUser = useAuthStore((state) => state.loggedInUser);
    const [imageSrc, setImageSrc] = useState('/empty.png');
    const [file, setFile] = useState('');

    if (!loggedInStatus) {
        history.push('/login');
    }

    const handleClick = () => {
        console.log(file);
        uploadFileApi(loggedInUser,file);
        alert('Upload successfully!');
    };

    const handleFileClick = (event) => {
        event.preventDefault();
        // setFile(event.target.value);
        setFile(document.getElementById('fileInput').files[0])
    };

    useEffect(() => {
        if(file !== ''){
            setImageSrc('/csv.png');
        }
        if(file === ''){
            setImageSrc('/empty.png');
        }
    }, [file]);


    const uploadFileApi = async (user, file) => {
        // const url = 'http://localhost:8000/api/dataset/';
        const url = new URL('http://localhost:8000/api/dataset/');
        url.searchParams.append('email', user);
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch(url, {
          method: 'post',
          body: formData,
        //   Authorization: `Bearer ${props.token}`
        });
        const data = await response.json();
        if (data.error) {
          alert(data.error);
        } else {
          alert('success!');
          // return true;
        }
      };

    return (
        <Container className="init-page-container">
            <Row>
                <Col className="col-2">
                    <SideBar />
                </Col>
                <Col className="col-10">
                    <h1>Upload data to initialise dataset</h1>
                    <img src={imageSrc} className='csv' alt="csv" />
                    <input type="file" className='select-file-button' onChange={handleFileClick} id="fileInput"></input>
                    <button className='upload-file-button' onClick={handleClick}>Upload a file</button>
                </Col>
            </Row>
        </Container>
    );
}

export default InitPage;
