from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from materials.models import Section, Material
from materials.serializer import SectionSerializer, MaterialSerializer

User = get_user_model()


class SectionModelTest(APITestCase):
    """Тесты для модели Section."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

    def test_create_section(self):
        """Тест создания раздела."""

        section = Section.objects.create(
            name="Test Section", description="Test Description", owner=self.user
        )

        self.assertEqual(section.name, "Test Section")
        self.assertEqual(section.description, "Test Description")
        self.assertEqual(section.owner, self.user)


class MaterialModelTest(APITestCase):
    """Тесты для модели Material."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

        self.section = Section.objects.create(name="Test Section", owner=self.user)

    def test_create_material(self):
        """Тест создания материала."""

        material = Material.objects.create(
            name="Test Material",
            description="Test Material Description",
            section=self.section,
            owner=self.user,
        )

        self.assertEqual(material.name, "Test Material")
        self.assertEqual(material.description, "Test Material Description")
        self.assertEqual(material.section, self.section)
        self.assertEqual(material.owner, self.user)

    def test_material_section_relationship(self):
        """Тест связи материала с разделом."""

        material = Material.objects.create(
            name="Test Material", section=self.section, owner=self.user
        )

        self.assertEqual(material.section, self.section)
        self.assertIn(material, self.section.materials.all())


class SectionSerializerTest(APITestCase):
    """Тесты для SectionSerializer."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

    def test_section_serializer(self):
        """Тест сериализации раздела."""

        section = Section.objects.create(
            name="Test Section", description="Test Description", owner=self.user
        )

        serializer = SectionSerializer(section)
        data = serializer.data

        self.assertEqual(data["id"], section.id)
        self.assertEqual(data["name"], "Test Section")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["owner"], self.user.id)

    def test_section_deserializer(self):
        """Тест десериализации раздела."""

        data = {
            "name": "New Section",
            "description": "New Description",
            "owner": self.user.id,
        }

        serializer = SectionSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        section = serializer.save()
        self.assertEqual(section.name, "New Section")
        self.assertEqual(section.owner, self.user)


class MaterialSerializerTest(APITestCase):
    """Тесты для MaterialSerializer."""

    def setUp(self):
        self.user = User.objects.create(email="teacher@test.com", role="teacher")
        self.user.set_password("teacher123")
        self.user.save()

        self.section = Section.objects.create(name="Test Section", owner=self.user)

    def test_material_serializer(self):
        """Тест сериализации материала."""

        material = Material.objects.create(
            name="Test Material",
            description="Test Description",
            section=self.section,
            owner=self.user,
        )

        serializer = MaterialSerializer(material)
        data = serializer.data

        self.assertEqual(data["id"], material.id)
        self.assertEqual(data["name"], "Test Material")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["section"], self.section.id)
        self.assertEqual(data["owner"], self.user.id)


class SectionViewSetTest(APITestCase):
    """Тесты для SectionViewSet."""

    def setUp(self):

        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")
        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")

        self.teacher_user = User.objects.create(
            email="teacher@test.com", role="teacher"
        )
        self.teacher_user.set_password("teacher123")
        self.teacher_user.save()

        self.teacher_user.groups.add(self.teacher_group)

        self.student_user = User.objects.create(
            email="student@test.com", role="student"
        )
        self.student_user.set_password("student123")
        self.student_user.save()

        self.student_user.groups.add(self.student_group)

        self.admin_user = User.objects.create(email="admin@test.com", role="admin")
        self.admin_user.set_password("admin123")
        self.admin_user.save()

        self.admin_user.groups.add(self.admin_group)

        self.section = Section.objects.create(
            name="Test Section", description="Test Description", owner=self.teacher_user
        )

        self.section_list_url = reverse("materials:section-list")
        self.section_detail_url = reverse(
            "materials:section-detail", kwargs={"pk": self.section.id}
        )

    def test_list_sections_as_teacher(self):
        """Тест получения списка разделов преподавателем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(self.section_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Section")

    def test_list_sections_as_student(self):
        """Тест получения списка разделов студентом HTTP_403_FORBIDDEN."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.section_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_section_as_teacher(self):
        """Тест создания раздела преподавателем HTTP_201_CREATED."""

        self.client.force_authenticate(user=self.teacher_user)
        data = {"name": "New Section", "description": "New Description"}
        response = self.client.post(self.section_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 2)
        self.assertEqual(
            Section.objects.get(name="New Section").owner, self.teacher_user
        )

    def test_create_section_as_student(self):
        """Тест создания раздела студентом HTTP_403_FORBIDDEN."""

        self.client.force_authenticate(user=self.student_user)
        data = {"name": "New Section"}
        response = self.client.post(self.section_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_section_as_owner(self):
        """Тест получения раздела владельцем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(self.section_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Section")

    def test_update_section_as_owner(self):
        """Тест обновления раздела владельцем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        data = {"name": "Updated Section"}
        response = self.client.patch(self.section_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.section.refresh_from_db()
        self.assertEqual(self.section.name, "Updated Section")

    def test_delete_section_as_owner(self):
        """Тест удаления раздела владельцем HTTP_204_NO_CONTENT."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.delete(self.section_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации HTTP_401_UNAUTHORIZED."""

        response = self.client.get(self.section_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MaterialViewSetTest(APITestCase):
    """Тесты для MaterialViewSet."""

    def setUp(self):

        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.teacher_user = User.objects.create(
            email="teacher@test.com", role="teacher"
        )
        self.teacher_user.set_password("teacher123")
        self.teacher_user.save()

        self.teacher_user.groups.add(self.teacher_group)

        self.student_user = User.objects.create(
            email="student@test.com", role="student"
        )
        self.student_user.set_password("student123")
        self.student_user.save()

        self.student_user.groups.add(self.student_group)

        self.section = Section.objects.create(
            name="Test Section", owner=self.teacher_user
        )

        self.material = Material.objects.create(
            name="Test Material",
            description="Test Description",
            section=self.section,
            owner=self.teacher_user,
        )

        self.material_list_url = reverse("materials:material-list")
        self.material_detail_url = reverse(
            "materials:material-detail", kwargs={"pk": self.material.id}
        )

    def test_list_materials_as_teacher(self):
        """Тест получения списка материалов преподавателем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(self.material_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Material")

    def test_list_materials_as_student(self):
        """Тест получения списка материалов студентом HTTP_200_OK."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.material_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_material_as_teacher(self):
        """Тест создания материала преподавателем HTTP_201_CREATED."""

        self.client.force_authenticate(user=self.teacher_user)
        data = {
            "name": "New Material",
            "description": "New Description",
            "section": self.section.id,
        }
        response = self.client.post(self.material_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 2)
        self.assertEqual(
            Material.objects.get(name="New Material").owner, self.teacher_user
        )

    def test_create_material_as_student(self):
        """Тест создания материала студентом HTTP_403_FORBIDDEN."""
        self.client.force_authenticate(user=self.student_user)
        data = {"name": "New Material", "section": self.section.id}
        response = self.client.post(self.material_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_material_as_owner(self):
        """Тест получения материала владельцем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get(self.material_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Material")

    def test_retrieve_material_as_student(self):
        """Тест получения материала студентом HTTP_200_OK."""

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.material_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Material")

    def test_update_material_as_owner(self):
        """Тест обновления материала владельцем HTTP_200_OK."""

        self.client.force_authenticate(user=self.teacher_user)
        data = {"name": "Updated Material"}
        response = self.client.patch(self.material_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material.refresh_from_db()
        self.assertEqual(self.material.name, "Updated Material")

    def test_update_material_as_student(self):
        """Тест обновления материала студентом HTTP_403_FORBIDDEN."""

        self.client.force_authenticate(user=self.student_user)
        data = {"name": "Updated Material"}
        response = self.client.patch(self.material_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_material_as_owner(self):
        """Тест удаления материала владельцем HTTP_204_NO_CONTENT."""

        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.delete(self.material_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Material.objects.count(), 0)

    def test_unauthorized_access(self):
        """Тест доступа без авторизации HTTP_401_UNAUTHORIZED."""

        response = self.client.get(self.material_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
