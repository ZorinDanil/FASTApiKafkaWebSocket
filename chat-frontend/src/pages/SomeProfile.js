import React, { useEffect, useState } from 'react';
import { get_profile } from '../api/Profile';
import { useParams } from 'react-router-dom';
import { Box, Spinner, Avatar, Heading, Text, Stack, Flex, Divider, Center } from '@chakra-ui/react';
import 'react-datepicker/dist/react-datepicker.css';

function SomeProfilePage() {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const params = useParams()
  const userId = params.user_id;

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await get_profile(userId);
        setProfile(response);
      } catch (error) {
        console.error('Error fetching profile:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [userId]);


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
    <Box maxW="3xl" mx="auto" p="6" borderWidth="1px" borderRadius="lg" overflow="hidden" bg="white" boxShadow="md">
        <>
          <Flex mb="4" alignItems="center">
            <Avatar size="2xl" name={profile.name} src={`data:image/jpeg;base64,${profile.profile_picture_url}`} />
            <Box ml="4">
                <>
               
                  <Heading as="h2" size="lg">{profile.name} {profile.lastname}</Heading>
                  <Text fontSize="md" color="gray.500">День рождения: {new Date(profile.birthday).toLocaleDateString()}</Text>
                </>
            </Box>
          </Flex>
          <Divider mb="4" />
          <Stack spacing={4}>
            <Text>ID Пользователя: {profile.user_id}</Text>
            <Text fontSize="md" >Дата создания Профиля: {new Date(profile.created_at).toLocaleDateString()}</Text>

          </Stack>
 
        </>
    </Box>
  );
};

export default SomeProfilePage;
