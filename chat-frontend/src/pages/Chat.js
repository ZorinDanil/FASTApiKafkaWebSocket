import React, {useState, useEffect, useRef } from 'react';
import { Box, Flex, Input, Button, Text, HStack, Avatar, useToast } from '@chakra-ui/react';
import { getToken, getUserId } from '../utils/auth';
import { useParams, Link } from 'react-router-dom';

import { get_profile } from '../api/Profile';
import { get_chat_messages } from '../api/Chat';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const userId = getUserId();
  const [username, setUsername] = useState('');
  const [profilePictureUrl, setProfilePictureUrl] = useState('');
  const params = useParams();
  const chatId = params.chat_id;
  const toast = useToast();
  const messagesEndRef = useRef(null);
  const ws = useRef(null);
  const token = getToken();
  const profilesCache = useRef(new Map());

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await get_profile(userId);
        setUsername(profile.name);
        setProfilePictureUrl(profile.profile_picture_url);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, [userId]);

  useEffect(() => {
    const fetchProfiles = async (senderIds) => {
      const profilePromises = senderIds.map(async (senderId) => {
        if (!profilesCache.current.has(senderId)) {
          const profile = await get_profile(senderId);
          profilesCache.current.set(senderId, profile);
        }
        return profilesCache.current.get(senderId);
      });

      await Promise.all(profilePromises);
    };

    const fetchMessages = async () => {
      try {
        const messages = await get_chat_messages(chatId, token);
        const senderIds = Array.from(new Set(messages.map(message => message.sender_id)));

        await fetchProfiles(senderIds);

        const messagesWithProfiles = messages.map(message => {
          const profile = profilesCache.current.get(message.sender_id);
          return {
            ...message,
            senderName: profile.name,
            senderProfilePicture: profile.profile_picture_url,
          };
        });

        setMessages(messagesWithProfiles);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };

    fetchMessages();
  }, [chatId, token]);

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket(`ws://localhost:8002/chat/api/v1/ws/${chatId}?token=${token}`);

      ws.current.onopen = () => {
        toast({
          title: 'Connected to chat server.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      };

      ws.current.onmessage = async (event) => {
        const message = JSON.parse(event.data);

        if (message.chat_id !== chatId) {
          return; // Ignore messages from other chats
        }

        if (!profilesCache.current.has(message.sender_id)) {
          const profile = await get_profile(message.sender_id);
          profilesCache.current.set(message.sender_id, profile);
        }

        const { name: senderName, profile_picture_url: senderProfilePicture } = profilesCache.current.get(message.sender_id);
        setMessages((prevMessages) => [...prevMessages, { ...message, senderName, senderProfilePicture }]);
      };
    };

    connectWebSocket();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [chatId, token, toast]);

  const handleSendMessage = () => {
    if (newMessage.trim() === '') return;
    const message = {
      content: newMessage,
      sender_id: userId,
      chat_id: chatId, // Add chat_id to the message
    };
    ws.current.send(JSON.stringify(message));
    setNewMessage('');
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Box maxW="5xl" mx="auto" p="6" borderWidth="1px" borderRadius="lg" overflow="hidden" bg="white" boxShadow="md">
      <Flex direction="column" height="80vh">
        <Flex mb="4" alignItems="center">
          <Avatar size="lg" name={username} src={`data:image/jpeg;base64,${profilePictureUrl}`} />
          <Box ml="4">
            <Text fontSize="xl" fontWeight="bold">{username}</Text>
          </Box>
        </Flex>
        <Box flex="1" overflowY="auto" p="4" borderWidth="1px" borderRadius="lg">
          {messages.map(({ senderName, senderProfilePicture, content, timestamp, sender_id }, index) => (
            <HStack key={index} align="start" mb="4" bg={index % 2 === 0 ? 'blue.100' : 'gray.100'} p="4" borderRadius="lg">
              <Avatar name={senderName} src={`data:image/jpeg;base64,${senderProfilePicture}`} />
              <Box>
                <Link to={`/profile/${sender_id}`}>
                <Text fontWeight="bold">{senderName}</Text>
                </Link>
                <Text>{content}</Text>
                <Text fontSize="xs" color="gray.500">{new Date(timestamp).toLocaleTimeString()}</Text>
              </Box>
            </HStack>
          ))}
          <div ref={messagesEndRef} />
        </Box>
        <Flex mt="4">
          <Input
            placeholder="Type your message..."
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            mr="2"
          />
          <Button onClick={handleSendMessage} colorScheme="blue">Send</Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default ChatPage;
