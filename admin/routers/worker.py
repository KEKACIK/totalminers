import logging

from flask import Blueprint, request, render_template, redirect, url_for, flash

from admin import service
from admin.db.database import basic_get, basic_create, basic_get_all, basic_delete
from admin.db.models import User, Worker, MinerItem
from admin.modules.headframe import headframe_api
from admin.service import generate_user_dict
from admin.utils import auth_required, HashRateTypes

workers_router = Blueprint('workers_router', 'workers_router')


@workers_router.get('/workers/<id>/')
@auth_required
def users_workers_page(id: int):
    user = basic_get(User, id=id)
    workers = {}
    workers_frame = headframe_api.get_miner_workers(user.miner_id)
    for worker in workers_frame:
        if not workers.get(worker['id']):
            workers[worker['id']] = {
                'id': worker['id'],
                'name': None,
                'type': None,
                'status': None,
                'frame': False,
                'db': False,
            }
        workers[worker['id']]['name'] = worker['name']
        workers[worker['id']]['type'] = worker['type']
        workers[worker['id']]['status'] = worker['status']
        workers[worker['id']]['frame'] = True
    for worker in basic_get_all(Worker, user_id=user.id):
        if not workers.get(worker.worker_id):
            workers[worker.worker_id] = {
                'id': worker.worker_id,
                'name': None,
                'type': None,
                'status': None,
                'frame': False,
                'db': False,
            }
        workers[worker.worker_id]['name'] = worker.worker_name
        workers[worker.worker_id]['db'] = True
    logging.critical(workers)
    return render_template(
        'users_workers.html',
        user=generate_user_dict(user=user),
        workers=[worker for _, worker in workers.items()],
    )


@workers_router.get('/workers/<id>/create')  # BOUNDARY CREATE
@auth_required
def create_boundary(id):
    user = basic_get(User, id=id)
    return render_template('worker_create_boundary.html', user=generate_user_dict(user=user))


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
        return redirect(url_for('workers_router.create_boundary', id=id))
    if basic_get(Worker, user_id=user.id, worker_name=name):
        flash(f'У пользователя уже есть воркер с названием "{name}"!')
        return redirect(url_for('workers_router.init_real', id=id))
    try:
        hash_rate = int(hash_rate)
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
    boundary_id = headframe_api.create_boundary(
        name=name,
        recipient_miner_id=user.miner_id,
        donor_miner_id=donor_miner_id,
        hash_rate=HashRateTypes().get(hash_type),
    )
    basic_create(
        Worker,
        user_id=user.id,
        miner_item_id=miner_item.id,
        worker_id=boundary_id,
        worker_name=name,
        hashrate=hash_rate,
    )
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.get('/workers/<id>/init_real')  # REAL INIT
@auth_required
def init_real(id: int):
    user = basic_get(User, id=id)
    return render_template('worker_init_real.html', user=generate_user_dict(user=user))


@workers_router.post('/workers/<id>/init_real')  # REAL INIT
@auth_required
def init_real_post(id):
    user = basic_get(User, id=id)
    name = request.form.get('name')
    miner_id = request.form.get('miner_id')
    miner_item_id = request.form.get('miner_item_id')
    if '' in [name, miner_id, miner_item_id]:
        flash('Поля не заполнены!')
        return redirect(url_for('workers_router.init_real', id=id))
    if basic_get(Worker, worker_id=miner_id):
        flash('Воркер с таким worker_id уже создан!')
        return redirect(url_for('workers_router.init_real', id=id))
    if basic_get(Worker, user_id=user.id, worker_name=name):
        flash('У пользователя уже есть воркер с таким названием!')
        return redirect(url_for('workers_router.init_real', id=id))
    miner_item = basic_get(MinerItem, id=int(miner_item_id))
    if not miner_item:
        flash('Майнер не найден!')
        return redirect(url_for('workers_router.init_real', id=id))
    basic_create(
        Worker,
        user_id=user.id,
        item_name=miner_item.name,
        miner_item_id=miner_item.id,
        worker_id=miner_id,
        worker_name=name,
    )
    return redirect(url_for('workers_router.users_workers_page', id=id))


@workers_router.get('/workers/<id>/delete')
@auth_required
def delete_worker(id: int):
    worker_id = request.args.get('worker_id')
    worker = basic_get(Worker, worker_id=worker_id)
    headframe_api.delete_boundary(worker_id=worker_id)
    basic_delete(Worker, id_=worker.id)
    return redirect(url_for('workers_router.users_workers_page', id=id))
