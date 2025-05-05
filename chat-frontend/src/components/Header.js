import React, { useState, useEffect } from "react";
import {
  Box,
  Stack,
  Heading,
  Flex,
  ButtonGroup,
  Button,
  useDisclosure
} from "@chakra-ui/react";
import { Link } from "react-router-dom";

import RegisterModal from "./Register";
import LoginModal from "./Login";
import { getToken, removeToken } from "../utils/auth";

function Header(props){
    const { isOpen, onOpen, onClose } = useDisclosure();
    const handleToggle = () => (isOpen ? onClose() : onOpen());
    const [isAuthenticated, setIsAuthenticated] = useState(!!getToken());
    const [registerModalIsOpen, setRegisterModalIsOpen] = useState(false);
    const [loginModalIsOpen, setLoginModalIsOpen] = useState(false);
  
    const openRegisterModal = () => {
      setRegisterModalIsOpen(true);
    };
  
    const openLoginModal = () => {
      setLoginModalIsOpen(true);
    };
  
    const closeModal = () => {
      setRegisterModalIsOpen(false);
      setLoginModalIsOpen(false);
    };

  
    useEffect(() => {
      setIsAuthenticated(!!getToken());
      setRegisterModalIsOpen(false);
      setLoginModalIsOpen(false);
    }, [isAuthenticated]);
  
    useEffect(() => {
      if (!loginModalIsOpen) {
        setIsAuthenticated(!!getToken());
      }
    }, [loginModalIsOpen]);

      
    useEffect(() => {
        if (!registerModalIsOpen) {
          setIsAuthenticated(!!getToken());
        }
      }, [registerModalIsOpen]);
    
  
    const handleLogout = () => {
      removeToken();
      setIsAuthenticated(false);
    };
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding={6}
      bg="teal.500"
      color="white"
      {...props}
    >
      <Flex align="center" mr={5}>
        <Link to='/'>
        <Heading as="h1" size="lg" letterSpacing={"tighter"}>
          WebSocket Chat
        </Heading>
        </Link>
      </Flex>

      <Box display={{ base: "block", md: "none" }} onClick={handleToggle}>
      </Box>

      <Stack
        direction={{ base: "column", md: "row" }}
        display={{ base: isOpen ? "block" : "none", md: "flex" }}
        width={{ base: "full", md: "auto" }}
        alignItems="center"
        flexGrow={1}
        mt={{ base: 4, md: 0 }}
      >
      </Stack>

      <Box
        display={{ base: isOpen ? "block" : "none", md: "block" }}
        mt={{ base: 4, md: 0 }}
      >
{!isAuthenticated ? (
  <ButtonGroup variant='outline' spacing='6'>
    <Button colorScheme='teal' variant='solid' onClick={openRegisterModal}>
      Создать аккаунт
    </Button>
    <Button colorScheme='teal' variant='solid' onClick={openLoginModal}>
      Войти
    </Button>
  </ButtonGroup>
) : (
    <ButtonGroup variant='outline' spacing='6'>

    <Button colorScheme='teal' variant='solid' onClick={handleLogout}>
      Выход
    </Button>
    <Link to="/profile/me">

      <Button colorScheme='teal' variant='solid'>
      Профиль
    </Button>
    </Link>

    <Link to="/users">

  <Button colorScheme='teal' variant='solid'>
  Пользователи
  </Button>
  </Link>
    </ButtonGroup>
)}


        <RegisterModal isOpen={registerModalIsOpen} onClose={closeModal}/>
        <LoginModal isOpen={loginModalIsOpen} onClose={closeModal}/>
      </Box>
    </Flex>
  );
};

export default Header;
