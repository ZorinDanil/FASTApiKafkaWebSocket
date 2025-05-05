import React, { useEffect, useState, forwardRef } from 'react';
import { get_profile, update_profile } from '../api/Profile';
import { getUserId } from '../utils/auth';
import { useToast, Box, Spinner, Skeleton, Avatar, Heading, Text, Stack, Flex, Divider, Button, Center, Input } from '@chakra-ui/react';
import { MdCalendarToday } from 'react-icons/md';
import { useDropzone } from 'react-dropzone';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const ProfilePage = () => {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editableProfile, setEditableProfile] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const userId = getUserId();
  const toast = useToast();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await get_profile(userId);
        setProfile(response);
        setEditableProfile(response);
      } catch (error) {
        console.error('Error fetching profile:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [userId]);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditableProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value,
    }));
  };

  const handleDateChange = (date) => {
    setEditableProfile((prevProfile) => ({
      ...prevProfile,
      birthday: date,
    }));
  };

  const handleSaveClick = async () => {
    try {
      if (selectedFile) {
        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
          editableProfile.profile_picture_url = base64String;

          await update_profile(userId, editableProfile);
          setProfile(editableProfile);
          toast({
            title: 'Профиль обновлен.',
            status: 'success',
            duration: 5000,
            isClosable: true,
          });
          setIsEditing(false);
        };
        reader.readAsDataURL(selectedFile);
      } else {
        await update_profile(userId, editableProfile);
        setProfile(editableProfile);
        toast({
          title: 'Профиль обновлен.',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
        setIsEditing(false);
      }
    } catch (err) {
      toast({
        title: 'Ошибка обновления профиля.',
        description: err.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleDrop = (acceptedFiles) => {
    setSelectedFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop: handleDrop });

  const CustomDateInput = forwardRef(({ value, onClick }, ref) => (
    <Button onClick={onClick} ref={ref} leftIcon={<MdCalendarToday />}>
      {value || 'Выберите дату'}
    </Button>
  ));

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
      {profile ? (
        <>
          <Flex mb="4" alignItems="center">
            <Avatar size="2xl" name={profile.name} src={`data:image/jpeg;base64,${profile.profile_picture_url}`} />
            <Box ml="4">
              {isEditing ? (
                <>
                <Stack spacing={2}>
                <Text fontSize="md">Имя</Text>

                  <Input
                    name="name"
                    value={editableProfile.name}
                    onChange={handleInputChange}
                    placeholder="Имя"
                    mb="2"
                  />
                  <Text fontSize="md">Фамилия</Text>

                  <Input
                    name="lastname"
                    value={editableProfile.lastname}
                    onChange={handleInputChange}
                    placeholder="Фамилия"
                    mb="2"
                  />
                  <Text fontSize="md">День рождения</Text>
                  <Box mb="2">
                    <DatePicker
                      selected={new Date(editableProfile.birthday)}
                      onChange={handleDateChange}
                      dateFormat="yyyy-MM-dd"
                      customInput={<CustomDateInput />}
                    />
                  </Box>
                  <Text fontSize="md">Фотография профиля</Text>
                  <Box {...getRootProps()} borderWidth="2px" borderRadius="lg" p="6" borderColor="gray.300" borderStyle="dashed">
                    <input {...getInputProps()} />
                    <p>Перетащите фото сюда или нажмите для выбора файла</p>
                    {selectedFile && <Text mt="2">Выбранный файл: {selectedFile.name}</Text>}
                  </Box>
                  </Stack>

                </>
              ) : (
                <>
                  <Heading as="h2" size="lg">{profile.name} {profile.lastname}</Heading>
                  <Text fontSize="md" color="gray.500">День рождения: {new Date(profile.birthday).toLocaleDateString()}</Text>
                </>
              )}
            </Box>
          </Flex>
          <Divider mb="4" />
          <Stack spacing={4}>
            <Text>ID Пользователя: {profile.user_id}</Text>
            <Text fontSize="md" >Дата создания Профиля: {new Date(profile.created_at).toLocaleDateString()}</Text>

          </Stack>
          {isEditing ? (
            <Button mt="4" colorScheme="green" onClick={handleSaveClick}>Сохранить</Button>
          ) : (
            <Button mt="4" colorScheme="blue" onClick={handleEditClick}>Изменить</Button>
          )}
        </>
      ) : (
        <Skeleton height="20px" my="10px" />
      )}
    </Box>
  );
};

export default ProfilePage;
