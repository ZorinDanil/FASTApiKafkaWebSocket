import React, { useState, useEffect } from 'react';
import { Box, VStack, HStack, Avatar, Text, Spinner, Center, Button, useToast } from '@chakra-ui/react';
import { getToken } from '../utils/auth';
import { get_all_profiles } from '../api/Profile';
import { get_chat_by_participants, create_chat } from '../api/Chat';
import { useNavigate } from 'react-router-dom';

const UsersPage = () => {
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const toast = useToast();
  const token = getToken();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const usersList = await get_all_profiles(token);
        setUsers(usersList);
      } catch (error) {
        toast({
          title: 'Failed to fetch users.',
          description: error.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsers();
  }, [token, toast]);

  const handleSendMessage = async (participantId) => {
    try {
      const participants = [participantId];
      let chat;
      try {
        chat = await get_chat_by_participants(participants, token);
        chat = chat[0]
      } catch {
        chat = await create_chat(participants, token);
      }
      navigate(`/chat/${chat.id}`);
    } catch (error) {
      toast({
        title: 'Failed to initiate chat.',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (isLoading) {
    return (
      <Center minHeight="100vh">
        <Spinner
          thickness="4px"
          speed="0.65s"
          emptyColor="gray.200"
          color="blue.500"
          size="xl"
        />
      </Center>
    );
  }

  return (
    <Box maxW="5xl" mx="auto" p="6" borderWidth="1px" borderRadius="lg" overflow="hidden" bg="white" boxShadow="md">
      <VStack spacing="4" align="stretch">
        {users.map((user) => (
          <HStack key={user.id} align="start" p="4" borderRadius="lg" bg="gray.100">
            <Avatar name={user.name} src={`data:image/jpeg;base64,${user.profile_picture_url}`} />
            <Box>
                <Text>ID: {user.user_id}</Text>
              <Text fontWeight="bold">{user.name}</Text>
              <Text>{user.email}</Text>
            </Box>
            <Button onClick={() => handleSendMessage(user.user_id)} colorScheme="blue" ml="auto">
              Отправить сообщение
            </Button>
          </HStack>
        ))}
      </VStack>
    </Box>
  );
};

export default UsersPage;
