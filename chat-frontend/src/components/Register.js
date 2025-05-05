import React, { useState } from 'react';
import { register, login } from '../api/Auth';
import { useToast, Text, Stack, Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter, Button, Input, InputGroup, InputRightElement } from '@chakra-ui/react';
import { setToken, setUserId } from '../utils/auth';

function RegisterForm({onClose, }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await register(username, email, password);
      toast({
        title: 'Регистрация прошла успешно!',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      try {
        const response = await login(username, password);
          setToken(response.access_token);
          setUserId(response.id);
          onClose();
      } catch (err) {
        
      }
    } catch (err) {
      toast({
        title: 'Ошибка регистрации.',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };


  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing={3}>
        <Text fontSize='md'>Логин</Text>
        <Input placeholder='Логин' size='md' value={username} onChange={(e) => setUsername(e.target.value)} required/>

        <Text fontSize='md'>Почта</Text>
        <Input placeholder='Почта' size='md' value={email} onChange={(e) => setEmail(e.target.value)} required />

        <Text fontSize='md'>Пароль</Text>
        <InputGroup size='md'>
          <Input
            pr='4.5rem'
            type={showPassword ? 'text' : 'password'}
            placeholder='Пароль' required onChange={(e) => setPassword(e.target.value)}
          />
          <InputRightElement width='4.5rem'>
            <Button h='1.75rem' size='sm' onClick={handlePasswordVisibility}>
              {showPassword ? 'Hide' : 'Show'}
            </Button>
          </InputRightElement>
        </InputGroup>
      <Button type="submit">Register</Button>

      </Stack>
    </form>
  );
}

function RegisterModal({ isOpen, onClose }) {
  return (
    <div>
            <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Регистрация</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <RegisterForm onClose={onClose}/>
          </ModalBody>
          <ModalFooter>

          </ModalFooter>
        </ModalContent>
      </Modal>
    </div>
  )
}
export default RegisterModal;