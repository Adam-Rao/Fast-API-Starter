from typing import List, Optional
from fastapi import HTTPException, status, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func
from app import models, oauth2
from app.schemas import Post, PostCreate, PostOut
from app.database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0,
              search: Optional[str] = ''):

    posts = db.query(models.Posts, func.count(models.Vote.post_id).label(
        'votes')).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
        models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts, func.count(models.Vote.post_id).label(
        'votes')).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
        models.Posts.owner_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return


@router.put('/{id}', response_model=Post)
def update_post(id: int,
                post: PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform this action')

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    updated_post = post_query.first()

    return updated_post
