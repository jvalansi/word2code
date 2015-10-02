'''
Created on Aug 16, 2015

@author: jordan
'''
import numpy as np
from sklearn.externals.joblib.parallel import Parallel, delayed
# online learning:
#     try to use decrease when wrong
#         check whether the problem is solved, if not, decrease joint feature
#     increase when right
#         check whether the problem is solved, if does, increase joint feature
#    check whether comes closer to the golden Y



def online_learn(X, Y, learner, initialize=True):
        """Learn parameters using structured perceptron.

        Parameters
        ----------
        X : iterable
            Traing instances. Contains the structured input objects.
            No requirement on the particular form of entries of X is made.

        Y : iterable
            Training labels. Contains the strctured labels for inputs in X.
            Needs to have the same length as X.

        initialize : boolean, default=True
            Whether to initialize the model for the data.
            Leave this true except if you really know what you are doing.
        """
        if initialize:
            learner.model.initialize(X, Y)        
        size_joint_feature = learner.model.size_joint_feature
        learner.w = np.zeros(size_joint_feature)
        if learner.average is not False:
            if learner.average is True:
                learner.average = 0
            elif learner.average < -1:
                raise NotImplemented("The only negative value for averaging "
                                     "implemented at the moment is `-1`. Try "
                                     "`max_iter - k` but be aware of the "
                                     "possibility of early stopping.")
            w_bar = np.zeros(size_joint_feature)
            n_obs = 0
        learner.loss_curve_ = []
        max_losses = np.sum([learner.model.max_loss(y) for y in Y])
        try:
            for iteration in xrange(learner.max_iter):
                if learner.average == -1:
                    # By resetting at every iteration we effectively get
                    # averaging over the last one.
                    n_obs = 0
                    w_bar.fill(0)
                effective_lr = ((iteration + learner.decay_t0) **
                                learner.decay_exponent)
                losses = 0
                if learner.verbose:
                    print("iteration %d" % iteration)
                if learner.batch:
                    Y_hat = (Parallel(n_jobs=learner.n_jobs)(
                        delayed(learner.model.inference)(learner.model, x, learner.w) for x, y in
                        zip(X, Y)))
                    for x, y, y_hat in zip(X, Y, Y_hat):
                        current_loss = learner.model.loss(y, y_hat)
                        losses += current_loss
                        if current_loss:
                            learner.w += effective_lr * (learner.model.joint_feature(x, y) -
                                                      learner.model.joint_feature(x, y_hat))
                    if learner.average is not False and iteration >= learner.average:
                        n_obs += 1
                        w_bar = ((1 - 1. / n_obs) * w_bar +
                                 (1. / n_obs) * learner.w)
                else:
#                         # standard online update
#                     for x, y in zip(X, Y):
#                         y_hat = learner.model.inference(x, learner.w)
#                         current_loss = learner.model.loss(y, y_hat)
#                         losses += current_loss
#                         if current_loss:
#                             learner.w += effective_lr * (learner.model.joint_feature(x, y) -
#                                                       learner.model.joint_feature(x, y_hat))
#                         if (learner.average is not False and
#                                 iteration >= learner.average):
#                             print('in n_obs update')
#                             n_obs += 1
#                             w_bar = ((1 - 1. / n_obs) * w_bar +
#                                      (1. / n_obs) * learner.w)
                    (learner, losses, effective_lr) = online_update(X, Y, learner, losses, effective_lr)
                learner.loss_curve_.append(float(losses) / max_losses)
                if learner.verbose:
                    print("avg loss: %f w: %s" % (learner.loss_curve_[-1],
                                                  str(learner.w)))
                    print("effective learning rate: %f" % effective_lr)
                if learner.loss_curve_[-1] == 0:
                    if learner.verbose:
                        print("Loss zero. Stopping.")
                    break

        except KeyboardInterrupt:
            pass
        finally:
            if learner.average is not False:
                learner.w = w_bar
        return learner


def online_update(X, Y, learner, losses, effective_lr):
# def online_update(X, Y, learner, losses, effective_lr, iteration, n_obs, w_bar):
        # standard online update
    for x, y in zip(X, Y):
        y_hat = learner.model.inference(x, learner.w)
        current_loss = learner.model.loss(y, y_hat)
        losses += current_loss
        if current_loss:
            learner.w += effective_lr * (learner.model.joint_feature(x, y) -
                                      learner.model.joint_feature(x, y_hat))
#         if (learner.average is not False and
#                 iteration >= learner.average):
#             n_obs += 1
#             w_bar = ((1 - 1. / n_obs) * w_bar +
#                      (1. / n_obs) * learner.w)
    return (learner, losses, effective_lr)


def online_update_from_examples(X, Y_good, Y_bad, learner, losses, effective_lr):
# def online_update(X, Y, learner, losses, effective_lr, iteration, n_obs, w_bar):
        # standard online update
    for x, y_good, y_bad in zip(X, Y_good, Y_bad):
        current_loss = learner.model.loss(y_good, y_bad)
        losses += current_loss
        if current_loss:
            learner.w += effective_lr * (learner.model.joint_feature(x, y_good) -
                                      learner.model.joint_feature(x, y_bad))
#         if (learner.average is not False and
#                 iteration >= learner.average):
#             n_obs += 1
#             w_bar = ((1 - 1. / n_obs) * w_bar +
#                      (1. / n_obs) * learner.w)
    return (learner, losses, effective_lr)
