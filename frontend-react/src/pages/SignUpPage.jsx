/* eslint-disable react/no-unescaped-entities */
import { Container } from "react-bootstrap";
import { useEffect, useState } from 'react';
import axios from 'axios'
import { useHistory } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function SignUpPage() {
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [questions, setQuestions] = useState([]);
  const [question_id_1, setquestion_id_1] = useState('');
  const [answer_1, setAnswer_1] = useState('');
  const [question_id_2, setQuestion_id_2] = useState('');
  const [answer_2, setAnswer_2] = useState('');


  useEffect(  () => {
    const fetchData = async () => {
      if (import.meta.env.MODE === 'development') {
        setQuestions([[1,"What is your favorite color?"],[2,"What is your favorite food?"]]);
        return;
      }

      const allQuestions = await axios.get(`${import.meta.env.VITE_API_URL}/api/Authentication/GetAllQuestions`);
      if (allQuestions.status === 200) {
        const questionsList = Object.keys(allQuestions.data).map((key) => [key, allQuestions.data[key]]);
        setQuestions(questionsList);
      } 
    }
    fetchData();
    }, []);
    console.log(questions)

  const registerUser = async (email, password, question_id_1, answer_1, question_id_2, answer_2) => {
    try {

      if (import.meta.env.MODE === 'development') {
        return true;
      }

      const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/Authentication/signup`, {
        email,
        password,
        question_id_1,
        answer_1,
        question_id_2,
        answer_2
      }).catch((error) => {
        alert(error.response.data.error);
        return false;
      });
      if (response.status === 201) {
        alert("User registered successfully")
        return true;
      } 
    } catch (error) {
      return false;
    }
  };

  const validatePassword = () => {
    return password === confirmPassword;
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validatePassword()) {
      alert('Passwords do not match');
      return;
    }

    const isRegistered = await registerUser(email, password, question_id_1, answer_1, question_id_2, answer_2);
    if (isRegistered) {
      history.push('/login');
    }
  }



  return (
    <div>
      <Container>
      <h1>SignUp</h1>
      <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email"  value={email} onChange={(e) => setEmail(e.target.value)}/>
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
        </Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
        <Form.Text className="text-muted">
          Password must be longer than 8 characters, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.
        </ Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Confirm Password</Form.Label>
        <Form.Control type="password" placeholder="Confirm password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formSecurityQuestion1">
        <Form.Label>Security Question 1</Form.Label>

        <Form.Select aria-label="Question 1" value={question_id_1} onChange={(e) => setquestion_id_1(e.target.value)}>
          <option>Open this select menu</option>
          {questions.map((question) => {
            console.log(question)
            return <option key={question[0]} value={question[0]}>{question[1]}</option>
          })}
        </Form.Select>

        <Form.Control type="text" placeholder="Enter answer to question 1" value={answer_1} onChange={(e) => setAnswer_1(e.target.value)} />

      </Form.Group>

      <Form.Group className="mb-3" controlId="formSecurityQuestion2">
        <Form.Label>Security Question 2</Form.Label>

        <Form.Select aria-label="Question 2" value={question_id_2} onChange={(e) => setQuestion_id_2(e.target.value)} >
          <option>Open this select menu</option>
          {questions.map((question) => {
            return <option key={question[0]} value={question[0]}>{question[1]}</option>
          })}
        </Form.Select>

        <Form.Control type="text" placeholder="Enter answer to question 2" value={answer_2} onChange={(e) => setAnswer_2(e.target.value)} />
      </Form.Group>

      <Button variant="primary" type="submit" onClick={handleSubmit}>
        Sign Up
      </Button>
    </Form>
      </Container>
    </div>
  );
}

export default SignUpPage;