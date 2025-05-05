import { login } from '../api/Auth';

import React, { useState } from 'react';
import {setToken, setUserId} from '../utils/auth';
import { useToast, Text, Stack, Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter, Button, Input, InputGroup, InputRightElement } from '@chakra-ui/react';


function LoginForm({onClose}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const toast = useToast();
  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await login(username, password);
        setToken(response.access_token);
        setUserId(response.id);
        onClose();
    } catch (err) {
      toast({
        title: 'Ошибка входа.',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing={3}>

        <Text fontSize='md'>Логин</Text>
        <Input placeholder='Логин' size='md' value={username} onChange={(e) => setUsername(e.target.value)} required />

        <Text fontSize='md'>Пароль</Text>
        <InputGroup size='md'>
          <Input
            pr='4.5rem'
            type={showPassword ? 'text' : 'password'}
            placeholder='Пароль' required
            onChange={(e) => setPassword(e.target.value)}
          />
          <InputRightElement width='4.5rem'>
            <Button h='1.75rem' size='sm' onClick={handlePasswordVisibility}>
              {showPassword ? 'Hide' : 'Show'}
            </Button>
          </InputRightElement>
        </InputGroup>
      <Button type="submit">Войти</Button>

      </Stack>
    </form>
  );
}

function LoginModal({ isOpen, onClose,  }) {
    return (
      <div>
              <Modal isOpen={isOpen} onClose={onClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Вход</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <LoginForm onClose={onClose}/>
            </ModalBody>
            <ModalFooter>
  
            </ModalFooter>
          </ModalContent>
        </Modal>
      </div>
    )
  }
export default LoginModal;
