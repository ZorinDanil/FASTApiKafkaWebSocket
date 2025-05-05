import * as React from 'react'
import { ChakraProvider } from '@chakra-ui/react'
import ProfilePage from './pages/Profile';
import SomeProfilePage from './pages/SomeProfile'
import BasePage from './pages/Base';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ChatPage from './pages/Chat';
import UsersPage from './pages/Users';

const App = () => {
  return (
    <ChakraProvider>
      <Router>
        <Layout>
          <Routes>
          <Route path="/profile/me" element={<ProfilePage />} />
          <Route path="/profile/:user_id" element={<SomeProfilePage />} />
          <Route path='/users' element={<UsersPage/>}/>
            <Route path="/" element={<BasePage />} />
            <Route path="/chat/:chat_id" element={<ChatPage />} />
            <Route path='/users' element={<UsersPage/>}/>
          </Routes>
        </Layout>
      </Router>
    </ChakraProvider>
  );
}

export default App;