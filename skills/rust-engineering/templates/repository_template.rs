// SQLx Repository Pattern Template
use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;

pub struct UserEntity {
    pub id: Uuid,
    pub username: String,
    pub email: String,
}

#[async_trait]
pub trait UserRepository: Send + Sync {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<UserEntity>, sqlx::Error>;
    async fn save(&self, user: &UserEntity) -> Result<(), sqlx::Error>;
}

pub struct PgUserRepository {
    pool: PgPool,
}

impl PgUserRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl UserRepository for PgUserRepository {
    async fn find_by_id(&self, id: Uuid) -> Result<Option<UserEntity>, sqlx::Error> {
        let record = sqlx::query_as!(
            UserEntity,
            r#"
            SELECT id, username, email
            FROM users
            WHERE id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await?;

        Ok(record)
    }

    async fn save(&self, user: &UserEntity) -> Result<(), sqlx::Error> {
        sqlx::query!(
            r#"
            INSERT INTO users (id, username, email)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO UPDATE
            SET username = EXCLUDED.username, email = EXCLUDED.email
            "#,
            user.id,
            user.username,
            user.email
        )
        .execute(&self.pool)
        .await?;

        Ok(())
    }
}
