import logging

from flask import Blueprint, request, render_template, redirect, url_for, flash

from admin.db.database import basic_get, basic_create, basic_get_all, basic_update
from admin.db.models import User, Worker, MinerItem
from admin.modules.headframe import headframe_api
from admin.service import generate_user_dict, generate_miner_worker_dict
from admin.utils import auth_required, HashRateTypes

workers_router = Blueprint('workers_router', 'workers_router')


@workers_router.get('/workers/<id>/')
@auth_required
def users_workers_page(id: int):
    user = basic_get(User, id=id)
    workers_db = basic_get_all(Worker, user_id=user.id)
    workers_site = headframe_api.get_miner_workers(user.miner_id)
    workers_statuses = {}
    for worker_site in workers_site.get('data', []):
        workers_statuses[worker_site['id']] = worker_site['status']

    return render_template(
        'users_workers.html',
        user=generate_user_dict(user=user),
        workers=[
            generate_miner_worker_dict(worker=worker, workers_statuses=workers_statuses)
            for worker in workers_db
        ],
    )


@workers_router.get('/workers/<id>/create')  # BOUNDARY CREATE
@auth_required
def create_boundary(id):
    user = basic_get(User, id=id)
    return render_template(
        'worker_create_boundary.html',
        user=generate_user_dict(user=user),
        hash_types=HashRateTypes().get_all(),
    )


@workers_router.post('/workers/<id>/create')  # BOUNDARY CREATE
@auth_required
def create_boundary_post(id: int):
    user = basic_get(User, id=id)
    name = request.form.get('name')
    donor_miner_id = request.form.get('donor_miner_id')
    hash_rate = request.form.get('hash_rate')
    hash_type = request.form.get('hash_type')
    miner_item_id = request.form.get('miner_item_id')
    if '' in [name, donor_miner_id, miner_item_id, hash_rate, hash_type]:
        flash(f'Все поля должны быть заполнены')
        return redirect(url_for('workers_router.create_boundary', id=id))
    if basic_get(Worker, user_id=user.id, name=name):
        flash(f'У пользователя уже есть воркер с названием "{name}"!')
        return redirect(url_for('workers_router.init_real', id=id))
    try:
        hash_rate = int(hash_rate) * HashRateTypes().get(hash_type)
    except:
        flash('Поле "Хэшрейт" должно быть числом')
        return redirect(url_for('workers_router.create_boundary', id=id))
    if hash_rate < 4294967296:
        flash('Поле "Хэшрейт" минимальное значение 4.29 GH/s')
        return redirect(url_for('workers_router.create_boundary', id=id))
    miner_item = basic_get(MinerItem, id=int(miner_item_id))
    if not miner_item:
        flash('Поле "ID Товара (майнера)" товар не найден')
        return redirect(url_for('workers_router.create_boundary', id=id))
    logging.critical(dict(
        name=name,
        recipient_miner_id=user.miner_id,
        donor_miner_id=donor_miner_id,
        hash_rate=hash_rate,
        hash_type=hash_type,
    ))
    boundary = headframe_api.create_boundary(
        name=name,
        recipient_miner_id=user.miner_id,
        donor_miner_id=donor_miner_id,
        hash_rate=str(hash_rate),
    )
    if boundary.get('error'):
        flash(f'Ошибка: {boundary}')
        return redirect(url_for('workers_router.create_boundary', id=id))
    basic_create(
        Worker,
        id_str=boundary['id'],
        name=boundary['name'],
        behavior=boundary['behavior'],
        user_id=user.id,
        miner_item_id=miner_item.id,
        hidden=False,
    )
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.get('/workers/<id>/delete')
@auth_required
def delete_worker(id: int):
    worker = basic_get(Worker, id=request.args.get('worker_id'))
    boundary = headframe_api.delete_boundary(worker_id=worker.id_str)
    if boundary.get('error'):
        flash(f'Ошибка: {boundary}')
        return redirect(url_for('workers_router.users_workers_page', id=id))
    basic_update(worker, hidden=True)
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.get('/workers/<id>/update')
@auth_required
def update_worker(id: int):
    worker = basic_get(Worker, id=request.args.get('worker_id'))
    type_ = request.args.get('type')
    if type_ == 'hidden_true':
        basic_update(worker, hidden=True)
    elif type_ == 'hidden_false':
        basic_update(worker, hidden=False)
    return redirect(url_for('workers_router.users_workers_page', id=id))
