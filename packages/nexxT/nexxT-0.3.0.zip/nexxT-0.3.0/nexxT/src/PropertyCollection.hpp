/* 
 * SPDX-License-Identifier: Apache-2.0
 * Copyright (C) 2020 ifm electronic gmbh
 *
 * THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
 */

#ifndef NEXXT_PROPERTY_COLLECTION_HPP
#define NEXXT_PROPERTY_COLLECTION_HPP

#include <QtCore/QObject>
#include <QtCore/QVariant>
#include "NexxTLinkage.hpp"

namespace nexxT
{
    class DLLEXPORT PropertyHandler
    {        
    public:
        PropertyHandler();
        virtual ~PropertyHandler();
        virtual QVariantMap options();
        virtual QVariant fromConfig(const QVariant &value);
        virtual QVariant toConfig(const QVariant &value);
        virtual QVariant toViewValue(const QVariant &value);
        virtual QWidget *createEditor(QWidget *parent);
        virtual void setEditorData(QWidget *editor, const QVariant &value);
        virtual QVariant getEditorData(QWidget *editor);
    };

    class DLLEXPORT PropertyCollection : public QObject
    {
        Q_OBJECT

    public:
        PropertyCollection();
        virtual ~PropertyCollection();

        virtual void defineProperty(const QString &name, const QVariant &defaultVal, const QString &helpstr);
        virtual void defineProperty(const QString &name, const QVariant &defaultVal, const QString &helpstr, const QVariantMap &options);
        virtual void defineProperty(const QString &name, const QVariant &defaultVal, const QString &helpstr, const PropertyHandler *handler);
        virtual QVariant getProperty(const QString &name) const;

    public slots:
        virtual void setProperty(const QString &name, const QVariant &variant);
        virtual QString evalpath(const QString &path) const;

    signals:
        void propertyChanged(const PropertyCollection &sender, const QString &name);
    };
};

#endif
