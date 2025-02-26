import { Button, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function SideBar() {
  return (
    <Nav className="flex-column" style={{ 
      paddingTop: '76px', 
      backgroundColor: '#82ADDC',
      height: '100vh',
      position: 'fixed',
      top: 0,
      left: 0,
      width: '150px'
    }}>
      <Link to="/data/initialisation" className="mb-0" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          textAlign: 'center', 
          padding: '10px 0',
          borderBottom: '1px solid #00BFFF'
        }}>
          <div><img src="/uploadfile.png" alt="Upload" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>Upload Data</div>
        </Button>
      </Link>
      
      <Link to="/data/view" className="mb-0" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          textAlign: 'center', 
          padding: '10px 0',
          borderBottom: '1px solid #00BFFF'
        }}>
          <div><img src="/viewdata.png" alt="Viewdata" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>View Data</div>
        </Button>
      </Link>

      <Link to="/data/anomalies" className="mb-0" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          textAlign: 'center', 
          padding: '10px 0',
          borderBottom: '2px solid #00BFFF'
        }}>
          <div><img src="/anomalies.png" alt="Anomalies" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>View Anomalies</div>
        </Button>
      </Link>
    </Nav>
  );
}

export default SideBar;
